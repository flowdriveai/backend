from flask import Response
import json

class Respond(Response):
    def __init__(self, success: bool, message, data=None, status=200, headers=None, mimetype='application/json', content_type=None, direct_passthrough=False):
        _data = {'success': success, 'message': message}

        # Default to 400 if success is false
        if success == False and status == 200:
            status = 400

        if data:
            print("data updated:")
            print(data)
            _data.update(data)
        super().__init__(json.dumps(_data, indent=4, default=str), status=status, headers=headers, mimetype=mimetype, content_type=content_type, direct_passthrough=direct_passthrough)