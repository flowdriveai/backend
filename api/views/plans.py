from flask.views import MethodView

from api.utils.response import Respond
from api.models.models import Plans

class PlanController(MethodView):
    """
    Plans Resource
    """

    def get(self):
        plans = Plans.query.all()

        resp = []
        for plan in plans:
            resp.append({
                'name': plan.name,
                'cost': plan.credits,
                'key_required': plan.key_required
            })

        return Respond(
            success=True,
            message=resp
        )
