import os

from sqlalchemy import MetaData
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_mail import Mail

app = Flask(__name__)
CORS(app)

app_settings = os.getenv(
    'APP_SETTINGS',
    'api.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db, render_as_batch=True)
mail = Mail(app)

from api.views.urls import auth_bp, user_bp, drive_bp, health_bp, device_bp, plans_bp
from api.cli import cli_bp

app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(drive_bp)
app.register_blueprint(device_bp)
app.register_blueprint(health_bp)
app.register_blueprint(plans_bp)
app.register_blueprint(cli_bp)
