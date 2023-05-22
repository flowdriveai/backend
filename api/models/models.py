import jwt
import datetime

import shortuuid

from api import app, db, bcrypt

class Plans(db.Model):
    """Flowpilot Plans"""
    __tablename__ = "plans"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(12), unique=True, nullable=False)
    name = db.Column(db.String(255), unique=True, nullable=False)
    ttl = db.Column(db.Integer, nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    key_required = db.Column(db.Boolean, nullable=False, default=False)
    max_devices = db.Column(db.Integer, nullable=False, default=1, server_default='1')

    def __init__(self, name, ttl, credits, key_required=False, max_devices=1):
        self.uid = shortuuid.ShortUUID().random(length=12)
        self.name = name
        self.ttl = ttl
        self.credits = credits
        self.key_required = key_required
        self.max_devices = max_devices


class PlanKeys(db.Model):
    """Plan Keys"""
    __tablename__ = "plan_keys"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(20), unique=True, nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'))
    sent = db.Column(db.Boolean, server_default='0', default=False)
    expired = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, plan_id):
        self.key = shortuuid.ShortUUID().random(length=20)
        self.plan_id = plan_id


class Subscriptions(db.Model):
    """Flowpilot Subscriptions"""
    __tablename__ = "subscriptions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(12), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'))
    plan_key_id = db.Column(db.Integer, db.ForeignKey('plan_keys.id'), nullable=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, plan_id, plan_ttl, user_id=None, plan_key_id=None):
        self.uid = shortuuid.ShortUUID().random(length=12)
        self.user_id = user_id
        self.plan_id = plan_id
        self.plan_key_id = plan_key_id
        self.start_date = datetime.datetime.now()
        self.end_date = datetime.datetime.now() + datetime.timedelta(0, plan_ttl)


class Drive(db.Model):
    """ Drives Model for storing drive related data"""
    __tablename__ = "drives"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(12), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    started_on = db.Column(db.DateTime, nullable=False)
    ended_on = db.Column(db.DateTime, nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'))
    shared = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, user_id, started_on, ended_on, device_id, shared=False):
        self.uid = shortuuid.ShortUUID().random(length=12)
        self.user_id = user_id
        self.started_on = started_on
        self.ended_on = ended_on
        self.device_id = device_id
        self.shared = shared


class Device(db.Model):
    """User devices"""
    __tablename__ = "devices"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(12), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    dongle_id = db.Column(db.String(255), unique=True, nullable=False)
    model_name = db.Column(db.String(255), nullable=False)

    def __init__(self, user_id, dongle_id, model_name):
        self.uid = shortuuid.ShortUUID().random(length=12)
        self.user_id = user_id
        self.dongle_id = dongle_id
        self.model_name = model_name


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(12), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    last_login_at = db.Column(db.DateTime, nullable=True)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscriptions.id'))

    def __init__(self, email, password, admin=False, confirmed=False, confirmed_on=None, last_login_at=None):
        self.uid = shortuuid.ShortUUID().random(length=12)
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.registered_on = datetime.datetime.now()
        self.admin = admin
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on
        self.last_login_at = last_login_at

        # Add default subscription
        community_plan = Plans.query.filter_by(name='community').first()
        subscription = Subscriptions(community_plan.id, community_plan.ttl)
        db.session.add(subscription)
        db.session.commit()

        self.subscription_id = subscription.id

    def encode_auth_token(self, user_id, long_living=False):
        """
        Generates the Auth Token
        """
        _days = 10 if not long_living else 365

        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=_days),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), algorithms=['HS256'])
            is_blacklisted_token = BlacklistJWT.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class BlacklistJWT(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistJWT.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False
