from flask.views import MethodView

from api.utils.decorators import jwt_required
from api.utils.response import Respond

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
        # Dummy data

        import shortuuid
        object = [
            {
                "name": "drive2",
                "timestamp": shortuuid.uuid(),
                "url": "https://fdusermedia.s3.ap-south-1.amazonaws.com/4bXwW2i7K29H/2022-12-11--14-42-55--0/video?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEK%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCmFwLXNvdXRoLTEiRzBFAiB%2FN7moj%2F3UoZbr8Vg8mNMb81qdVmpYwbAKLhqXkvkXagIhAIla6c%2BdKKOUSOPktyeZHc3M%2FV1TYlzoJZlCHuNPqisHKuQCCBgQABoMNzU4MDk5ODAzNDMzIgxY99SmvQswtPwnBXsqwQJ2PiUV0j79u9vZQlXXRZSHfbzzPoKznPyVvsbf5Ef0VHuR5Q5lBK8A12ifds6i4HZOcYl4AKWS4ae0Z6hvXBoV09M5SSHFbfgjumIpEbunLQ%2Ff4zikYMLmuEvcQss%2Bs0xrRCYiX3s71BH11VFJ9oYrF48LIVfCf14WIhDGoSFOUTmuKgFAhnGxOkH6Od1VFsz42DYU2fY3%2BgvXD4atdq9wS%2BP%2BKsGZSCp0%2BBreeKaCyRaiydj1KFWi%2BIH%2FU8Ph4tAOnr2r7qvcyrfnrPqVlrasuH3BRwOS5A7SNYmexuTAWzIvOPT33Sey9qOlA1JDgW4cFtNxXujKzI0mk7MUbcYvZqdztmyWp4PNcRBroYWpMKdiiVqv9HHVZW5APiDqha4DyPgHsuA3z4wjFQ8v33r3BsV0df%2FuNeoYDq85ALo2Xv0wjayQngY6swLMAlhqABhpgbNXLNey3jAgg2zx47CV5M%2F%2Bggpu8oTPq%2BlZ3DnkHDCvAewRUERKNLLqfEHagDSqDup%2Fm8VF5bpEBgRfo9Ke3z5OYKr82DfdivRfFEQ1WAA%2FhJvvyXbxh1KOFizzNybr6t1HGUGpe%2BCjSbancDaewR7dzvhPsw6%2BUEM8KFlNZoPnMRR9CT%2F%2FLaUet556js6x4PQai5wcQKkfGq1WRMwU1dwwhx2jZM97V1IJ11zUuUrgCg8D1v54wXkWM2m8p8Rp4y1yMWMxSlRFFMlFhpTx3sh4GIlRFII7dqg%2FAwKlDmZsVzLob3ILahpOAOzr6GB9hqrAwgNCJSv2WZasOos%2Feng7tdjZoQwXt4SUSNCTuO9QR1ynAjNUYTSU%2BiY7YURtzv%2Be6awxc%2BeDR7H5&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20230115T200351Z&X-Amz-SignedHeaders=host&X-Amz-Expires=43200&X-Amz-Credential=ASIA3BASE7UUS6L3ZYUE%2F20230115%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Signature=8bb360a9f1134dad7af07cf41597b0de306787f8cded317246deaea8cad39610",
                "s3_key": "long_s3_key"
            },
            {
                "name": "drive1",
                "timestamp": shortuuid.uuid(),
                "url": "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
                "s3_key": "long_s3_key"
            },
            {
                "name": "drive2",
                "timestamp": shortuuid.uuid(),
                "url": "https://fdusermedia.s3.ap-south-1.amazonaws.com/4bXwW2i7K29H/2022-12-11--14-42-55--0/video?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEK%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCmFwLXNvdXRoLTEiRzBFAiB%2FN7moj%2F3UoZbr8Vg8mNMb81qdVmpYwbAKLhqXkvkXagIhAIla6c%2BdKKOUSOPktyeZHc3M%2FV1TYlzoJZlCHuNPqisHKuQCCBgQABoMNzU4MDk5ODAzNDMzIgxY99SmvQswtPwnBXsqwQJ2PiUV0j79u9vZQlXXRZSHfbzzPoKznPyVvsbf5Ef0VHuR5Q5lBK8A12ifds6i4HZOcYl4AKWS4ae0Z6hvXBoV09M5SSHFbfgjumIpEbunLQ%2Ff4zikYMLmuEvcQss%2Bs0xrRCYiX3s71BH11VFJ9oYrF48LIVfCf14WIhDGoSFOUTmuKgFAhnGxOkH6Od1VFsz42DYU2fY3%2BgvXD4atdq9wS%2BP%2BKsGZSCp0%2BBreeKaCyRaiydj1KFWi%2BIH%2FU8Ph4tAOnr2r7qvcyrfnrPqVlrasuH3BRwOS5A7SNYmexuTAWzIvOPT33Sey9qOlA1JDgW4cFtNxXujKzI0mk7MUbcYvZqdztmyWp4PNcRBroYWpMKdiiVqv9HHVZW5APiDqha4DyPgHsuA3z4wjFQ8v33r3BsV0df%2FuNeoYDq85ALo2Xv0wjayQngY6swLMAlhqABhpgbNXLNey3jAgg2zx47CV5M%2F%2Bggpu8oTPq%2BlZ3DnkHDCvAewRUERKNLLqfEHagDSqDup%2Fm8VF5bpEBgRfo9Ke3z5OYKr82DfdivRfFEQ1WAA%2FhJvvyXbxh1KOFizzNybr6t1HGUGpe%2BCjSbancDaewR7dzvhPsw6%2BUEM8KFlNZoPnMRR9CT%2F%2FLaUet556js6x4PQai5wcQKkfGq1WRMwU1dwwhx2jZM97V1IJ11zUuUrgCg8D1v54wXkWM2m8p8Rp4y1yMWMxSlRFFMlFhpTx3sh4GIlRFII7dqg%2FAwKlDmZsVzLob3ILahpOAOzr6GB9hqrAwgNCJSv2WZasOos%2Feng7tdjZoQwXt4SUSNCTuO9QR1ynAjNUYTSU%2BiY7YURtzv%2Be6awxc%2BeDR7H5&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20230115T200351Z&X-Amz-SignedHeaders=host&X-Amz-Expires=43200&X-Amz-Credential=ASIA3BASE7UUS6L3ZYUE%2F20230115%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Signature=8bb360a9f1134dad7af07cf41597b0de306787f8cded317246deaea8cad39610",
                "s3_key": "long_s3_key"
            },
            {
                "name": "drive1",
                "timestamp": shortuuid.uuid(),
                "url": "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
                "s3_key": "long_s3_key"
            },
            {
                "name": "drive2",
                "timestamp": shortuuid.uuid(),
                "url": "https://fdusermedia.s3.ap-south-1.amazonaws.com/4bXwW2i7K29H/2022-12-11--14-42-55--0/video?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEK%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCmFwLXNvdXRoLTEiRzBFAiB%2FN7moj%2F3UoZbr8Vg8mNMb81qdVmpYwbAKLhqXkvkXagIhAIla6c%2BdKKOUSOPktyeZHc3M%2FV1TYlzoJZlCHuNPqisHKuQCCBgQABoMNzU4MDk5ODAzNDMzIgxY99SmvQswtPwnBXsqwQJ2PiUV0j79u9vZQlXXRZSHfbzzPoKznPyVvsbf5Ef0VHuR5Q5lBK8A12ifds6i4HZOcYl4AKWS4ae0Z6hvXBoV09M5SSHFbfgjumIpEbunLQ%2Ff4zikYMLmuEvcQss%2Bs0xrRCYiX3s71BH11VFJ9oYrF48LIVfCf14WIhDGoSFOUTmuKgFAhnGxOkH6Od1VFsz42DYU2fY3%2BgvXD4atdq9wS%2BP%2BKsGZSCp0%2BBreeKaCyRaiydj1KFWi%2BIH%2FU8Ph4tAOnr2r7qvcyrfnrPqVlrasuH3BRwOS5A7SNYmexuTAWzIvOPT33Sey9qOlA1JDgW4cFtNxXujKzI0mk7MUbcYvZqdztmyWp4PNcRBroYWpMKdiiVqv9HHVZW5APiDqha4DyPgHsuA3z4wjFQ8v33r3BsV0df%2FuNeoYDq85ALo2Xv0wjayQngY6swLMAlhqABhpgbNXLNey3jAgg2zx47CV5M%2F%2Bggpu8oTPq%2BlZ3DnkHDCvAewRUERKNLLqfEHagDSqDup%2Fm8VF5bpEBgRfo9Ke3z5OYKr82DfdivRfFEQ1WAA%2FhJvvyXbxh1KOFizzNybr6t1HGUGpe%2BCjSbancDaewR7dzvhPsw6%2BUEM8KFlNZoPnMRR9CT%2F%2FLaUet556js6x4PQai5wcQKkfGq1WRMwU1dwwhx2jZM97V1IJ11zUuUrgCg8D1v54wXkWM2m8p8Rp4y1yMWMxSlRFFMlFhpTx3sh4GIlRFII7dqg%2FAwKlDmZsVzLob3ILahpOAOzr6GB9hqrAwgNCJSv2WZasOos%2Feng7tdjZoQwXt4SUSNCTuO9QR1ynAjNUYTSU%2BiY7YURtzv%2Be6awxc%2BeDR7H5&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20230115T200351Z&X-Amz-SignedHeaders=host&X-Amz-Expires=43200&X-Amz-Credential=ASIA3BASE7UUS6L3ZYUE%2F20230115%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Signature=8bb360a9f1134dad7af07cf41597b0de306787f8cded317246deaea8cad39610",
                "s3_key": "long_s3_key"
            },
            {
                "name": "drive2",
                "timestamp": shortuuid.uuid(),
                "url": "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
                "s3_key": "long_s3_key"
            },
            {
                "name": "drive1",
                "timestamp": shortuuid.uuid(),
                "url": "https://fdusermedia.s3.ap-south-1.amazonaws.com/4bXwW2i7K29H/2022-12-11--14-42-55--0/video?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEK%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCmFwLXNvdXRoLTEiRzBFAiB%2FN7moj%2F3UoZbr8Vg8mNMb81qdVmpYwbAKLhqXkvkXagIhAIla6c%2BdKKOUSOPktyeZHc3M%2FV1TYlzoJZlCHuNPqisHKuQCCBgQABoMNzU4MDk5ODAzNDMzIgxY99SmvQswtPwnBXsqwQJ2PiUV0j79u9vZQlXXRZSHfbzzPoKznPyVvsbf5Ef0VHuR5Q5lBK8A12ifds6i4HZOcYl4AKWS4ae0Z6hvXBoV09M5SSHFbfgjumIpEbunLQ%2Ff4zikYMLmuEvcQss%2Bs0xrRCYiX3s71BH11VFJ9oYrF48LIVfCf14WIhDGoSFOUTmuKgFAhnGxOkH6Od1VFsz42DYU2fY3%2BgvXD4atdq9wS%2BP%2BKsGZSCp0%2BBreeKaCyRaiydj1KFWi%2BIH%2FU8Ph4tAOnr2r7qvcyrfnrPqVlrasuH3BRwOS5A7SNYmexuTAWzIvOPT33Sey9qOlA1JDgW4cFtNxXujKzI0mk7MUbcYvZqdztmyWp4PNcRBroYWpMKdiiVqv9HHVZW5APiDqha4DyPgHsuA3z4wjFQ8v33r3BsV0df%2FuNeoYDq85ALo2Xv0wjayQngY6swLMAlhqABhpgbNXLNey3jAgg2zx47CV5M%2F%2Bggpu8oTPq%2BlZ3DnkHDCvAewRUERKNLLqfEHagDSqDup%2Fm8VF5bpEBgRfo9Ke3z5OYKr82DfdivRfFEQ1WAA%2FhJvvyXbxh1KOFizzNybr6t1HGUGpe%2BCjSbancDaewR7dzvhPsw6%2BUEM8KFlNZoPnMRR9CT%2F%2FLaUet556js6x4PQai5wcQKkfGq1WRMwU1dwwhx2jZM97V1IJ11zUuUrgCg8D1v54wXkWM2m8p8Rp4y1yMWMxSlRFFMlFhpTx3sh4GIlRFII7dqg%2FAwKlDmZsVzLob3ILahpOAOzr6GB9hqrAwgNCJSv2WZasOos%2Feng7tdjZoQwXt4SUSNCTuO9QR1ynAjNUYTSU%2BiY7YURtzv%2Be6awxc%2BeDR7H5&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20230115T200351Z&X-Amz-SignedHeaders=host&X-Amz-Expires=43200&X-Amz-Credential=ASIA3BASE7UUS6L3ZYUE%2F20230115%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Signature=8bb360a9f1134dad7af07cf41597b0de306787f8cded317246deaea8cad39610",
                "s3_key": "long_s3_key"
            },
            {
                "name": "drive2",
                "timestamp": shortuuid.uuid(),
                "url": "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
                "s3_key": "long_s3_key"
            },
            {
                "name": "drive3",
                "timestamp": shortuuid.uuid(),
                "url": "https://fdusermedia.s3.ap-south-1.amazonaws.com/4bXwW2i7K29H/2022-12-11--14-42-55--0/video?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEK%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCmFwLXNvdXRoLTEiRzBFAiB%2FN7moj%2F3UoZbr8Vg8mNMb81qdVmpYwbAKLhqXkvkXagIhAIla6c%2BdKKOUSOPktyeZHc3M%2FV1TYlzoJZlCHuNPqisHKuQCCBgQABoMNzU4MDk5ODAzNDMzIgxY99SmvQswtPwnBXsqwQJ2PiUV0j79u9vZQlXXRZSHfbzzPoKznPyVvsbf5Ef0VHuR5Q5lBK8A12ifds6i4HZOcYl4AKWS4ae0Z6hvXBoV09M5SSHFbfgjumIpEbunLQ%2Ff4zikYMLmuEvcQss%2Bs0xrRCYiX3s71BH11VFJ9oYrF48LIVfCf14WIhDGoSFOUTmuKgFAhnGxOkH6Od1VFsz42DYU2fY3%2BgvXD4atdq9wS%2BP%2BKsGZSCp0%2BBreeKaCyRaiydj1KFWi%2BIH%2FU8Ph4tAOnr2r7qvcyrfnrPqVlrasuH3BRwOS5A7SNYmexuTAWzIvOPT33Sey9qOlA1JDgW4cFtNxXujKzI0mk7MUbcYvZqdztmyWp4PNcRBroYWpMKdiiVqv9HHVZW5APiDqha4DyPgHsuA3z4wjFQ8v33r3BsV0df%2FuNeoYDq85ALo2Xv0wjayQngY6swLMAlhqABhpgbNXLNey3jAgg2zx47CV5M%2F%2Bggpu8oTPq%2BlZ3DnkHDCvAewRUERKNLLqfEHagDSqDup%2Fm8VF5bpEBgRfo9Ke3z5OYKr82DfdivRfFEQ1WAA%2FhJvvyXbxh1KOFizzNybr6t1HGUGpe%2BCjSbancDaewR7dzvhPsw6%2BUEM8KFlNZoPnMRR9CT%2F%2FLaUet556js6x4PQai5wcQKkfGq1WRMwU1dwwhx2jZM97V1IJ11zUuUrgCg8D1v54wXkWM2m8p8Rp4y1yMWMxSlRFFMlFhpTx3sh4GIlRFII7dqg%2FAwKlDmZsVzLob3ILahpOAOzr6GB9hqrAwgNCJSv2WZasOos%2Feng7tdjZoQwXt4SUSNCTuO9QR1ynAjNUYTSU%2BiY7YURtzv%2Be6awxc%2BeDR7H5&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20230115T200351Z&X-Amz-SignedHeaders=host&X-Amz-Expires=43200&X-Amz-Credential=ASIA3BASE7UUS6L3ZYUE%2F20230115%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Signature=8bb360a9f1134dad7af07cf41597b0de306787f8cded317246deaea8cad39610",
                "s3_key": "long_s3_key"
            },
            {
                "name": "drive2",
                "timestamp": shortuuid.uuid(),
                "url": "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
                "s3_key": "long_s3_key"
            },
        ]

        return Respond(
            success=True,
            message=object)

class DriveController(MethodView):
    """
    User Single Drive Data Fetch Resource
    """

    decorators = [jwt_required]

    def get(self, user, jwt):
        # Dummy data

        import datetime
        object = [
            {
                "name": "drive1",
                "url": "https://fdusermedia.s3.ap-south-1.amazonaws.com/4bXwW2i7K29H/2022-12-11--14-42-55--0/video?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEK%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCmFwLXNvdXRoLTEiRzBFAiB%2FN7moj%2F3UoZbr8Vg8mNMb81qdVmpYwbAKLhqXkvkXagIhAIla6c%2BdKKOUSOPktyeZHc3M%2FV1TYlzoJZlCHuNPqisHKuQCCBgQABoMNzU4MDk5ODAzNDMzIgxY99SmvQswtPwnBXsqwQJ2PiUV0j79u9vZQlXXRZSHfbzzPoKznPyVvsbf5Ef0VHuR5Q5lBK8A12ifds6i4HZOcYl4AKWS4ae0Z6hvXBoV09M5SSHFbfgjumIpEbunLQ%2Ff4zikYMLmuEvcQss%2Bs0xrRCYiX3s71BH11VFJ9oYrF48LIVfCf14WIhDGoSFOUTmuKgFAhnGxOkH6Od1VFsz42DYU2fY3%2BgvXD4atdq9wS%2BP%2BKsGZSCp0%2BBreeKaCyRaiydj1KFWi%2BIH%2FU8Ph4tAOnr2r7qvcyrfnrPqVlrasuH3BRwOS5A7SNYmexuTAWzIvOPT33Sey9qOlA1JDgW4cFtNxXujKzI0mk7MUbcYvZqdztmyWp4PNcRBroYWpMKdiiVqv9HHVZW5APiDqha4DyPgHsuA3z4wjFQ8v33r3BsV0df%2FuNeoYDq85ALo2Xv0wjayQngY6swLMAlhqABhpgbNXLNey3jAgg2zx47CV5M%2F%2Bggpu8oTPq%2BlZ3DnkHDCvAewRUERKNLLqfEHagDSqDup%2Fm8VF5bpEBgRfo9Ke3z5OYKr82DfdivRfFEQ1WAA%2FhJvvyXbxh1KOFizzNybr6t1HGUGpe%2BCjSbancDaewR7dzvhPsw6%2BUEM8KFlNZoPnMRR9CT%2F%2FLaUet556js6x4PQai5wcQKkfGq1WRMwU1dwwhx2jZM97V1IJ11zUuUrgCg8D1v54wXkWM2m8p8Rp4y1yMWMxSlRFFMlFhpTx3sh4GIlRFII7dqg%2FAwKlDmZsVzLob3ILahpOAOzr6GB9hqrAwgNCJSv2WZasOos%2Feng7tdjZoQwXt4SUSNCTuO9QR1ynAjNUYTSU%2BiY7YURtzv%2Be6awxc%2BeDR7H5&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20230115T200351Z&X-Amz-SignedHeaders=host&X-Amz-Expires=43200&X-Amz-Credential=ASIA3BASE7UUS6L3ZYUE%2F20230115%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Signature=8bb360a9f1134dad7af07cf41597b0de306787f8cded317246deaea8cad39610"
            },
        ]

        return Respond(
            success=True,
            message=object)