import datetime

from flask import render_template, request, url_for
from flask.views import MethodView

from api import bcrypt, db, app
from api.models.models import User, BlacklistJWT
from api.utils.decorators import jwt_required
from api.utils.email import send_email, valid_email
from api.utils.email_token import confirm_token, generate_confirmation_token
from api.utils.response import Respond
from api.utils.sts import generate_sts

class ConfirmEmailTokenController(MethodView):
    """
    User Email Verfication
    """
    def post(self):
        params = request.get_json()
        email = params.get('email')

        user = User.query.filter_by(email=email).first()

        if not valid_email(email) or not user:
            return Respond(
                success=False,
                message="Invalid email"
            )

        if user.confirmed:
            return Respond(
                success=False,
                message="User email already verified"
            )
        else:
            # send confirmation email
            email_token = generate_confirmation_token(user.email)
            confirm_url = url_for('.confirm_controller', token=email_token, _external=True)
            email_message = render_template('confirm_email.html', confirm_url=confirm_url)
            email_subject = "Flowdrive Onboarding"
            send_email(user.email, email_subject, email_message)

            return Respond(
                success=True,
                message="Confirmation email sent"
            )

    # TODO: use client side views
    def get(self):
        token = request.args.get('token')
        message = ""

        try:
            email = confirm_token(token)
            user = User.query.filter_by(email=email).first_or_404()
            if user.confirmed:
                message = 'Account already confirmed. Please login.'
            else:
                user.confirmed = True
                user.confirmed_on = datetime.datetime.now()
                db.session.add(user)
                db.session.commit()
                message = 'You have confirmed your account. Thanks!'
        except:
            message = 'The confirmation link is invalid or has expired.'

        return f"<p>{message}</p>", 200


class RegisterController(MethodView):
    """
    User Registration Resource
    """
    def post(self):
        params = request.get_json()

        # check if user already exists
        user = User.query.filter_by(email=params.get('email')).first()
        if not user:
            try:
                if not valid_email(params.get('email')):
                    return Respond(
                        success=False,
                        message="Invalid Email"
                    )
                    
                user = User(
                    email=params.get('email'),
                    password=params.get('password'),
                    confirmed=False
                )

                # send confirmation email
                email_token = generate_confirmation_token(user.email)
                confirm_url = url_for('.confirm_controller', token=email_token, _external=True)
                email_message = render_template('confirm_email.html', confirm_url=confirm_url)
                email_subject = "Flowdrive Onboarding"
                send_email(user.email, email_subject, email_message)

                # insert the user
                db.session.add(user)
                db.session.commit()

                return Respond(
                    success=True,
                    status=201,
                    message='Successfully registered', 
                )
            except Exception as e:
                return Respond(
                    success=False,
                    message=e, 
                    status=500
                )
        else:
            return Respond(
                success=False,
                message='User already exists. Please Log in.', 
                status=202
            )


class LoginController(MethodView):
    """
    User Login Resource
    """
    def post(self):
        params = request.get_json()
        try:
            # fetch the user data
            user = User.query.filter_by(
                email=params.get('email')
            ).first()

            long_living = params['long_living'] if 'long_living' in params else False

            if not isinstance(long_living, bool):
                return Respond(
                    success=False,
                    message="`long_living` should be a valid boolean"
                )

            if user and bcrypt.check_password_hash(
                user.password, params.get('password')
            ):
                if not user.confirmed:
                    return Respond(
                        success=False,
                        message='User email not verified', 
                        status=401
                    )

                auth_token = user.encode_auth_token(user.id, long_living)
                if auth_token:
                    # Update last login
                    user.last_login_at = datetime.datetime.now()
                    db.session.commit()

                    return Respond(
                        success=True,
                        message={
                            'user_id': user.uid,
                            'auth_token': auth_token,
                        }, 
                    )
            else:
                return Respond(
                    success=False,
                    message='User email and password do not match',
                    status=401
                )

        except Exception as e:
            return Respond(
                success=False,
                message=e,
                status=500
            )

class STSController(MethodView):
    """
    AWS STS Tokens Resource
    """

    decorators = [jwt_required]

    def get(self, user, jwt):
        return Respond(
            success=True,
            message=generate_sts(user.uid)
        )

class JWTRefreshController(MethodView):
    """
    Refresh JWT Token
    """

    decorators = [jwt_required]

    def post(self, user, jwt):
        params = request.get_json()

        long_living = params['long_living'] if 'long_living' in params else False

        if not isinstance(long_living, bool):
            return Respond(
                success=False,
                message="`long_living` should be a valid boolean"
            )

        return Respond(
            success=True,
            message={
                'auth_token': user.encode_auth_token(user.id, long_living) 
        })

class ForgotPasswordController(MethodView):
    """
    Forgot Password
    """

    # TODO: Use client side views
    def post(self):
        params = request.get_json()
        email = params.get('email')

        user = User.query.filter_by(email=email).first()

        if not user:
            return Respond(
                success=False,
                message='Email does not exist'
            )
        elif not user.confirmed:
            return Respond(
                success=False,
                message='Please confirm your email first'
            )
        
        # Forge a request link, and send it to their email
        email_token = generate_confirmation_token(user.email)
        confirm_url = f"https://flicks.flowdrive.ai/auth/reset-password?token={email_token}"
        email_message = render_template('forgot_password.html', confirm_url=confirm_url)
        email_subject = "Reset your Flowdrive password"
        send_email(user.email, email_subject, email_message)

        return Respond(
            success=True,
            message="A reset link is sent to your email"
        )

    
class ResetPasswordController(MethodView):
    """
    Set a new password
    """

    # TODO: Use client side views
    def post(self):
        params = request.get_json()
        token = params.get('token')
        new_password = params.get('password')

        try:
            email = confirm_token(token)
        except:
            return Respond(
                success=False,
                message='Invalid or expired token'
            )

        # Update password
        user = User.query.filter_by(email=email).first_or_404()
        user.password = bcrypt.generate_password_hash(
            new_password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode() 
        db.session.commit()
        return Respond(
            success=True,
            message="Successfully changed password"
        )


class LogoutController(MethodView):
    """
    Logout Resource
    """

    decorators = [jwt_required]

    def post(self, user, jwt):
        blacklist_token = BlacklistJWT(token=jwt)
        try:
            # insert the token
            db.session.add(blacklist_token)
            db.session.commit()
            return Respond(
                success=True,
                message='Successfully logged out'
            )
        except Exception as e:
            return Respond(
                success=False,
                message=e
            )
