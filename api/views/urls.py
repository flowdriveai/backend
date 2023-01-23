from flask import Blueprint
from api.views.auth import RegisterController, LoginController, LogoutController, ConfirmEmailTokenController, STSController, JWTRefreshController, ForgotPasswordController, ResetPasswordController
from api.views.user import UserController, DriveController, DrivesListController

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
drives_list_view = DrivesListController.as_view('drives_list_controller')
drive_view = DriveController.as_view('drive_controller')
user_bp.add_url_rule('/user/status', view_func=user_view, methods=['GET'])
user_bp.add_url_rule('/user/drives_list', view_func=drives_list_view, methods=['GET'])
user_bp.add_url_rule('/user/drive', view_func=drive_view, methods=['GET'])
