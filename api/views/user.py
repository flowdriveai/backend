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
                'user_id': user.id,
                'email': user.email,
                'admin': user.admin,
                'registered_on': user.registered_on,
                'last_login_at': user.last_login_at
        })