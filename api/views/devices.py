from flask.views import MethodView
from flask import request

from api import db
from api.models.models import Device, User
from api.utils.decorators import jwt_required
from api.utils.response import Respond

class DeviceController(MethodView):
    """
    Device Resource
    """

    decorators = [jwt_required]

    def post(self, user, jwt):
        params = request.get_json()

        dongle_id = params.get('dongle_id')
        model_name = params.get('model_name')
        
        if db.session.query(Device.id).filter_by(dongle_id=dongle_id).first() is not None:
            return Respond(
                success=False,
                message="Device already registered. Please revoke its access on your dashboard to use flowpilot on it"
            )

        try:
            device = Device(
                user_id=user.id,
                dongle_id=dongle_id,
                model_name=model_name
            )

            db.session.add(device)
            db.session.commit()

            return Respond(
                success=True,
                status=201,
                message={
                    'device_id': device.uid
                },
            )
        except Exception as e:
            return Respond(
                success=False,
                message=e, 
                status=500
            )


    def get(self, user, jwt):
        device_list_filtered = Device.query.filter_by(user_id=user.id).with_entities(Device.uid, Device.model_name).all()

        resp = []
        for device in device_list_filtered:
            resp.append({
                'device_id': device.uid,
                'model_name': device.model_name,
            })

        return Respond(success=True, message=resp)


    def delete(self, user, jwt):
        """Revoke a device"""

        params = request.get_json()

        device_id = params.get('device_id')

        device = Device.query.filter_by(uid=device_id).first()

        if device is None or device.user_id != user.id:
            return Respond(
                success=False,
                message="User does not own this device"
            )

        try:
            db.session.delete(device)
            db.session.commit()

            return Respond(
                success=True,
                status=201,
                message='Revoked', 
            )
        except Exception as e:
            return Respond(
                success=False,
                message=e, 
                status=500
            )
