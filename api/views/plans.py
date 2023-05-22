from flask.views import MethodView
from flask import request
from api.utils.decorators import jwt_required
from api.utils.email import send_email

from api import db
from api.utils.response import Respond
from api.models.models import PlanKeys, Plans

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

class SendInvitesController(MethodView):
    """
    Send Plan keys
    """

    decorators = [jwt_required]

    def post(self, user, jwt):

        if not user.admin:
            return Respond(success=False, message="Unauthorized", status=401)

        params = request.get_json()
        requested_plan = params.get('plan')
        message = params.get('message')
        emails = params.get('emails')

        plan = Plans.query.filter_by(name=requested_plan).first()
        if plan is None or not plan.key_required:
            return Respond(
                success=False,
                message=f"Invalid plan: {requested_plan}"
            )

        if not isinstance(emails, list):
            return Respond(success=False, message="Invalid input: emails", status=400)

        for email in emails:
            plan_key = PlanKeys(plan.id)
            email_message = (
                "Thanks for your patience!\n"
                f"Here is the {plan.name} invite key:\n"
                "\n"
                f"      {plan_key.key}\n"
                "\n"
                f"go to your flicks account and enter this key in the {plan.name} section.\n"
                "\n"
                f"{message}\n"
                "\n"
                "Login with same account in app.\n"
                "\n"
                "Thanks,\n"
                "Flowdrive Team\n"
            )
            email_subject = f"Your keys for the {plan.name} plan"
            send_email(email, email_subject, plaintext=email_message)
            plan_key.sent = True
            db.session.add(plan_key)
            db.session.commit()

        return Respond(
            success=True,
            message=emails
        )