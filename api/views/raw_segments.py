from flask.views import MethodView
import boto3

from api.utils.decorators import jwt_required
from api.utils.response import Respond
from api.utils.sts import generate_sts

from datetime import datetime

class RawSegmentsController(MethodView):
    """
    Raw Segments resource
    """

    decorators = [jwt_required]

    def get(self, user, jwt):
        sts_creds = generate_sts(user.uid)
        s3_client=boto3.client(
            's3',
            aws_access_key_id=sts_creds["access_key"],
            aws_secret_access_key=sts_creds["secret_access_key"],
            aws_session_token=sts_creds["session_token"],
        )

        bucket = "fdusermedia"
        prefix = f"unprocessed/{user.uid}"
        resp_map = []

        try:
            objects = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
            for obj in objects['Contents']:
                key = obj['Key']
                if (key.endswith('mp4')):
                    qlog_key = key.replace('fcam.mp4', 'qlog.bz2')
                    fcam_url = s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': key})
                    qlog_url = s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': qlog_key})

                    print(key)
                    time_str_raw = '--'.join(key.split('/')[3].split('--')[:2])
                    print(time_str_raw)
                    datetime_object = datetime.strptime(time_str_raw, '%Y-%m-%d--%H-%M-%S.%f')

                    resp_map.append({
                        'time': datetime_object,
                        'fcam': fcam_url,
                        'qlog': qlog_url
                    })

            return Respond(
                success=True,
                message=resp_map
            )

        except Exception as e:
            return Respond(
                success=False,
                message=e
            )
            
