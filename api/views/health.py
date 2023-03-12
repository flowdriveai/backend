from flask.views import MethodView

from api.utils.response import Respond

class HealthController(MethodView):
    """
    App Health Resource
    """

    def get(self):
        return Respond(
            success=True,
            message={
                "status": "up"
       })
