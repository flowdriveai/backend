from flask import Blueprint
from api.views.auth import RegisterController, LoginController, LogoutController, ConfirmEmailTokenController, STSController, JWTRefreshController, ForgotPasswordController, ResetPasswordController
from api.views.user import UserController, DriveControllerV99, DrivesListControllerV99, SubscribeController
from api.views.drives import DriveController, DriveListController, ShareDriveController
from api.views.devices import DeviceController
from api.views.health import HealthController
from api.views.plans import PlanController, SendInvitesController
from api.views.raw_segments import RawSegmentsController

## Auth
auth_bp = Blueprint('auth', __name__)
# define the API resources
registration_view = RegisterController.as_view('register_controller')
login_view = LoginController.as_view('login_controller')
logout_view = LogoutController.as_view('logout_controller')
confirm_view = ConfirmEmailTokenController.as_view('confirm_controller')
sts_view = STSController.as_view('sts_controller')
jwt_refresh_view = JWTRefreshController.as_view('jwt_refresh_controller')
forgot_password_view = ForgotPasswordController.as_view('forgot_password_controller')
reset_password_view = ResetPasswordController.as_view('reset_password_controller')

# add Rules for API Endpoints
auth_bp.add_url_rule('/auth/register', view_func=registration_view, methods=['POST'])
auth_bp.add_url_rule('/auth/login', view_func=login_view, methods=['POST'])
auth_bp.add_url_rule('/auth/logout', view_func=logout_view, methods=['POST'])
auth_bp.add_url_rule('/auth/confirm', view_func=confirm_view, methods=['POST', 'GET'])
auth_bp.add_url_rule('/auth/sts', view_func=sts_view, methods=['GET'])
auth_bp.add_url_rule('/auth/refresh_token', view_func=jwt_refresh_view, methods=['POST'])
auth_bp.add_url_rule('/auth/forgot_password', view_func=forgot_password_view, methods=['POST'])
auth_bp.add_url_rule('/auth/reset_password', view_func=reset_password_view, methods=['POST'])

## User
user_bp = Blueprint('user', __name__)
user_view = UserController.as_view('user_controller')
subscribe_view = SubscribeController.as_view('subscribe_controller')
drives_list_view_v99 = DrivesListControllerV99.as_view('drives_list_controller_v99')
drive_view_v99 = DriveControllerV99.as_view('drive_controller_v99')
user_bp.add_url_rule('/user/status', view_func=user_view, methods=['GET'])
user_bp.add_url_rule('/user/drives_listV99', view_func=drives_list_view_v99, methods=['GET'])
user_bp.add_url_rule('/user/driveV99', view_func=drive_view_v99, methods=['POST'])
user_bp.add_url_rule('/user/subscribe', view_func=subscribe_view, methods=['POST', 'DELETE'])


## Drives
drive_bp = Blueprint('drive', __name__)
drive_view = DriveController.as_view('drive_controller')
drive_list_view = DriveListController.as_view('drive_list_controller')
share_drive_view = ShareDriveController.as_view('share_drive_controller')
drive_bp.add_url_rule('/drive', view_func=drive_view, methods=['GET', 'POST'])
drive_bp.add_url_rule('/drive/list', view_func=drive_list_view, methods=['GET'])
drive_bp.add_url_rule('/drive/share', view_func=share_drive_view, methods=['POST'])

## Devices
device_bp = Blueprint('device', __name__)
device_view = DeviceController.as_view('device_controller')
device_bp.add_url_rule('/device', view_func=device_view, methods=['GET', 'POST', 'DELETE'])

## Health
health_bp = Blueprint('health', __name__)
health_view = HealthController.as_view('health_controller')
health_bp.add_url_rule('/health', view_func=health_view, methods=['GET'])

## Plans
plans_bp = Blueprint('plan', __name__)
plans_view = PlanController.as_view('plans_controller')
send_invites_view = SendInvitesController.as_view('send_invites_controller')
plans_bp.add_url_rule('/plans', view_func=plans_view, methods=['GET'])
plans_bp.add_url_rule('/plans/send_invites', view_func=send_invites_view, methods=['POST'])

## Raw Segments
raw_segments_bp = Blueprint('raw_segments', __name__)
raw_segments_view = RawSegmentsController.as_view('raw_segments_controller')
raw_segments_bp.add_url_rule('/raw_segments', view_func=raw_segments_view, methods=['GET'])