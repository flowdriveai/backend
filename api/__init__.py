import os

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

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db) 
mail = Mail(app)

from api.views.urls import auth_bp, user_bp, drive_bp
from api.cli import cli_bp

app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(drive_bp)
app.register_blueprint(cli_bp)
