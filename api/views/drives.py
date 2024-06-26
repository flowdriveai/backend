from flask.views import MethodView
from flask import request
import boto3
from botocore.errorfactory import ClientError

from api import db
from api.models.models import Device, Drive, User
from api.utils.decorators import jwt_required
from api.utils.response import Respond
from api.utils.sts import generate_sts

class DriveController(MethodView):
    """
    Drives resource
    """
    
    decorators = [jwt_required]

    def get(self, user, jwt):
        drive_uid = request.args.get('drive_id')

        drive = Drive.query.filter_by(uid=drive_uid).first()
        device = Device.query.filter_by(id=drive.device_id).first()

        if drive is None:
            # Drive not found
            return Respond(success=False, message="Drive not found", status=404)
        elif drive.user_id != user.id and not drive.shared:
            # Drive found but it is not of the same user and it is not shared
            return Respond(success=False, message="Unauthorized", status=401)
        else:
            # Drive is either shared, or requested by the correct user

            _user = User.query.filter_by(id=drive.user_id).first()
            if _user is None:
                # Something is fucked up
                return Respond(success=False, message="Could not map the given user id")

            keys = {
                "qlog": f"processed/{_user.uid}/{drive.uid}/qlog",
                "fcam": f"processed/{_user.uid}/{drive.uid}/fcam.mp4",
                "ecam": f"processed/{_user.uid}/{drive.uid}/ecam.mp4"
            }

            bucket = "fdusermedia"

            sts_creds = generate_sts(_user.uid)
            s3_client=boto3.client(
                's3',
                aws_access_key_id=sts_creds["access_key"],
                aws_secret_access_key=sts_creds["secret_access_key"],
                aws_session_token=sts_creds["session_token"],
            )

            s3_urls = {}
            for asset, key in keys.items():
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
                s3_urls[asset] = presigned_url

            # Calculate drive duration
            duration_secs = (drive.ended_on - drive.started_on).total_seconds()
            if duration_secs > 3600:
                duration_str = f"{round(duration_secs // 3600)} hours and {round(duration_secs // 60)} minutes"
            else:
                duration_str = f"{round(duration_secs // 60)} minutes and {round(duration_secs % 60)} seconds"

            return Respond(
                success=True,
                message={
                    'drive_id': drive.uid,
                    'started_on': drive.started_on,
                    'ended_on': drive.ended_on,
                    'duration': duration_str,
                    'device_id': device.model_name,
                    'shared': drive.shared,
                    'owned': drive.user_id == user.id,
                    'url_matrix': s3_urls
            })

    def post(self, user, jwt):
        """Triggered by the processing lamdba, _not_ the client"""

        params = request.get_json()

        if not user.admin:
            return Respond(success=False, message="Unauthorized", status=401)

        started_on = params['started_on']
        ended_on = params['ended_on']
        device_id = params['device_id']
        _user_uid = params['user_id']

        _user = User.query.filter_by(uid=_user_uid).first()
        if _user is None:
            # Something is fucked up
            return Respond(success=False, message="Could not map the given user id")
        
        drive = Drive(
            user_id=_user.id,
            started_on=started_on,
            ended_on=ended_on,
            device_id=device_id
        )

        db.session.add(drive)
        db.session.commit()

        return Respond(
            success=True,
            message={
                'drive_id': drive.uid,
                'credentials': generate_sts(_user.uid)
        })


class DriveListController(MethodView):
    """
    Fetches a list of drives
    """

    decorators = [jwt_required]

    def get(self, user, jwt):
        drive_list_filtered = Drive.query.filter_by(user_id=user.id).with_entities(Drive.uid, Drive.started_on, Drive.ended_on, Drive.shared).all()

        resp = []
        for drive in drive_list_filtered:
            resp.append({
                'drive_id': drive.uid,
                'started_on': drive.started_on,
                'ended_on': drive.ended_on,
                'shared': drive.shared
            })

        return Respond(success=True, message=resp)


class ShareDriveController(MethodView):
    """
    Share a drive
    """

    decorators = [jwt_required]

    def post(self, user, jwt):
        params = request.get_json()

        shared = params.get('shared')
        drive_uid = params.get('drive_id')
        drive = Drive.query.filter_by(uid=drive_uid).first()

        if drive.user_id != user.id:
            return Respond(success=False, message="Unauthorized", status=401)
        
        drive.shared = shared
        db.session.commit()

        return Respond(
            success=True,
            message={
                'drive_id': drive.uid,
                'shared': drive.shared,
        })
