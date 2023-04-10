from datetime import datetime
import time

from flask.views import MethodView
from flask import request
import boto3
from botocore.errorfactory import ClientError

from api import db
from api.utils.decorators import jwt_required
from api.utils.response import Respond
from api.utils.sts import generate_sts
from api.models.models import Subscriptions, Plans, PlanKeys

class UserController(MethodView):
    """
    User Resource
    """

    decorators = [jwt_required]

    def get(self, user, jwt):
        subscription = Subscriptions.query.filter_by(id=user.subscription_id).first()
        plan = Plans.query.filter_by(id=subscription.plan_id).first()

        return Respond(
            success=True,
            message={
                'user_id': user.uid,
                'email': user.email,
                'admin': user.admin,
                'registered_on': user.registered_on,
                'last_login_at': user.last_login_at,
                'plan': plan.name,
                'plan_expires_at': subscription.end_date
        })

class SubscribeController(MethodView):
    """
    Subscribe to plans
    """

    decorators = [jwt_required]

    def delete(self, user, jwt):
        community_plan = Plans.query.filter_by(name='community').first()

        subscription = Subscriptions(community_plan.id, community_plan.ttl, user.id)
        db.session.add(subscription)
        db.session.commit()

        user.subscription_id = subscription.id
        db.session.add(user)
        db.session.commit()

        return Respond(
            success=True,
            message=f"Changed plan to community"
        )

    def post(self, user, jwt):
        params = request.get_json()

        requested_plan = params.get('plan')
        key = params.get('key')

        # Previous plan expired ?
        old_subscription = Subscriptions.query.filter_by(id=user.subscription_id).first()
        old_plan = Plans.query.filter_by(id=old_subscription.plan_id).first()
        if old_plan.name != 'community' and old_subscription.end_date > datetime.now():
            return Respond(
                success=False,
                message="Previous subscription hasn't expired or ended yet"
            )

        # Requested plan exists ?
        new_plan = Plans.query.filter_by(name=requested_plan).first()
        if new_plan is None:
            return Respond(
                success=False,
                message=f"Unknown plan: {requested_plan}"
            )

        # Same plan ?
        if old_plan.name == new_plan.name:
            #TODO: Implement plan renewing once payment is set up
            return Respond(
                success=True,
                message="Plan unchanged"
            )

        # Key required ?
        if new_plan.key_required:
            # Key none ?
            if key is None:
                return Respond(
                    success=False,
                    message="An access key is required for this plan"
                )

            plan_key = PlanKeys.query.filter_by(key=key).first()

            # Key valid ?
            if plan_key is None or plan_key.expired == True or plan_key.plan_id != new_plan.id:
                return Respond(
                    success=False,
                    message="Key invalid or expired"
                )

            # Subscribe plan for user
            subscription = Subscriptions(new_plan.id, new_plan.ttl, user.id, plan_key.id)
            db.session.add(subscription)
            db.session.commit()

            plan_key.expired = True
            db.session.add(plan_key)
            db.session.commit()

            user.subscription_id = subscription.id
            db.session.add(user)
            db.session.commit()

            return Respond(
                success=True,
                message=f"Changed plan to {new_plan.name}"
            )

        if new_plan.credits != 0:
            # TODO: Implement payments
            return Respond(
                success=False,
                message="Payments haven't been implemented :("
            )

            subscription = Subscriptions(new_plan.id, new_plan.ttl)
            db.session.add(subscription)
            db.session.commit()

            user.subscription_id = subscription.id
            db.session.add(user)
            db.session.commit()

        # Subscribing to a 0 credit plan
        subscription = Subscriptions(new_plan.id, new_plan.ttl, user.id)
        db.session.add(subscription)
        db.session.commit()

        user.subscription_id = subscription.id
        db.session.add(user)
        db.session.commit()

        return Respond(
            success=True,
            message=f"Changed plan to {new_plan.name}"
        )


class DrivesListControllerV99(MethodView):
    """
    User Drive Data Fetch Resource
    """

    decorators = [jwt_required]

    def get(self, user, jwt):
        bucket = "fdusermedia"
        prefix = f"processed/{user.uid}"
        sts_creds = generate_sts(user.uid)
        s3_client=boto3.client(
          's3',
          aws_access_key_id=sts_creds["access_key"],
          aws_secret_access_key=sts_creds["secret_access_key"],
          aws_session_token=sts_creds["session_token"],
        )

        resp_map = {}

        objects = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
        if 'Contents' in objects:
            for obj in objects['Contents']:
                key = obj['Key']
                if key[-1] != '/':
                    resp_prefix = '/'.join(key.split('/')[:3])
                    time_str_raw = '--'.join(key.split('/')[2].split('--')[:2])

                    try:
                        datetime_object = datetime.strptime(time_str_raw, '%Y-%m-%d--%H-%M-%S')
                        unixtime = str(time.mktime(datetime_object.timetuple()))
                        print(unixtime)
                        if time_str_raw not in resp_map:
                            resp_map[time_str_raw] = {
                                "timestamp": unixtime,
                                "fcam": f"{resp_prefix}/fcam.mp4",
                                "ecam": f"{resp_prefix}/ecam.mp4",
                                "qlog": f"{resp_prefix}/qlog",
                            }
                    except Exception as e:
                        print(e)
                        

        resp=list(resp_map.values())

        return Respond(
            success=True,
            message=resp)

class DriveControllerV99(MethodView):
    """
    User List of Drive Data Fetch Resource
    """

    decorators = [jwt_required]

    def post(self, user, jwt):
        params = request.get_json()
        keys = params.get('keys')

        bucket = "fdusermedia"

        sts_creds = generate_sts(user.uid)
        s3_client=boto3.client(
          's3',
          aws_access_key_id=sts_creds["access_key"],
          aws_secret_access_key=sts_creds["secret_access_key"],
          aws_session_token=sts_creds["session_token"],
        )

        ret = {}

        for key in keys:
            try:
                s3_client.head_object(Bucket=bucket, Key=key)
            except ClientError as e:
                return Respond(
                    success=False,
                    message=e.response['Error']['Message'],
                    status=e.response['Error']['Code'],
                )
            
            presigned_url = s3_client.generate_presigned_url(
                "get_object", Params={"Bucket": bucket, "Key": key}
            )
            ret[key] = presigned_url

        return Respond(
            success=True,
            message=ret)
