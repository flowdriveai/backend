import os
basedir = os.path.abspath(os.path.dirname(__file__))
database_base_path = 'sqlite:///' + os.path.join(basedir, 'db-data')


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 11
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # mail settings
    MAIL_SERVER = 'email-smtp.eu-west-1.amazonaws.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ['APP_MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['APP_MAIL_PASSWORD']
    MAIL_DEFAULT_SENDER = "FlowDrive <flowdrive@wantguns.dev>"
    MAIL_DEFAULT_SENDER = "FlowDrive <no_reply@flowdrive.ai>"


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = os.path.join(database_base_path, 'dev.sqlite')


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI =  os.path.join(database_base_path, 'test.sqlite')
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False
    SERVER_NAME = os.getenv('SERVER_NAME', None)
    SQLALCHEMY_DATABASE_URI =  os.path.join(database_base_path, 'prod.sqlite')

