from datetime import datetime
import time

from flask.views import MethodView
from flask import request
import boto3
from botocore.errorfactory import ClientError

from api.utils.decorators import jwt_required
from api.utils.response import Respond
from api.utils.sts import generate_sts

class UserController(MethodView):
    """
    User Resource
    """

    decorators = [jwt_required]

    def get(self, user, jwt):
        return Respond(
            success=True,
            message={
                'user_id': user.uid,
                'email': user.email,
                'admin': user.admin,
                'registered_on': user.registered_on,
                'last_login_at': user.last_login_at
        })

class DrivesListController(MethodView):
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

        resp=list(resp_map.values())

        return Respond(
            success=True,
            message=resp)

class DriveController(MethodView):
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
