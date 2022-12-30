from flask import request

from functools import wraps

from api.utils.response import Respond
from api.models.models import User

def jwt_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        headers = request.headers
        bearer = headers.get('Authorization')
        if bearer is None:
            return Respond(
                success=False,
                message="Unauthenticated",
                status=403,
            )

        bearer_split = bearer.split()
        if len(bearer_split) < 2:
            return Respond(
                success=False,
                message="Invalid Authentication header",
                status=403
            )

        jwt_token = bearer_split[1]

        resp = User.decode_auth_token(jwt_token)
        if not isinstance(resp, str):
            # Decoded successfully
            user = User.query.filter_by(id=resp).first()
            kwargs['user'] = user
            kwargs['jwt'] = jwt_token

            return view_func(*args, **kwargs)
        
        return Respond(
            success=False,
            status=403,
            message=resp
        )

    return wrapper

