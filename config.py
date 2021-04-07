from decouple import config
from dotenv import load_dotenv
import os
from datetime import timedelta


class Config(object):
    APP_NAME = os.environ.get("APP_NAME")
    FOOTER_NAME = os.environ.get("FOOTER_NAME")
    CREDIT = os.environ.get("APP_NAME")

    basedir = os.path.abspath(os.path.dirname(__file__))

    # Set up the App SECRET_KEY
    SECRET_KEY = config(os.environ.get("SECRET_KEY"), default='?\xbf,\xb4\x8d\xa3"<\x9c\xb0@\x0f5\xab,w\xee\x8d$0\x13\x8b83')

    # This will create a file in <app> FOLDER
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, os.environ.get("SQLITE_DATABASE_NAME"))
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")

    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    DEBUG = os.environ.get("DEBUG")

    # Recaptcha
    RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY")
    RECAPTCHA_PARAMETERS = {'hl': 'zh', 'render': 'explicit'}
    RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}

    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=int(os.environ.get("PERMANENT_SESSION_LIFETIME")))
    SESSION_REFRESH_EACH_REQUEST = os.environ.get("SESSION_REFRESH_EACH_REQUEST")
    SESSION_COOKIE_NAME = os.environ.get("APP_NAME")

    # Security
    SESSION_COOKIE_HTTPONLY = os.environ.get("SESSION_COOKIE_HTTPONLY")
    REMEMBER_COOKIE_HTTPONLY = os.environ.get("REMEMBER_COOKIE_HTTPONLY")
    REMEMBER_COOKIE_DURATION = timedelta(minutes=int(os.environ.get("REMEMBER_COOKIE_DURATION")))

    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')  # Path to .env file
    load_dotenv(dotenv_path)


class ProductionConfig(Config):
    DEBUG = False

    # PostgreSQL database
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        config( 'DB_ENGINE'   , default='postgresql'    ),
        config( 'DB_USERNAME' , default='alogtrading'       ),
        config( 'DB_PASS'     , default='pass'          ),
        config( 'DB_HOST'     , default='localhost'     ),
        config( 'DB_PORT'     , default=5432            ),
        config( 'DB_NAME'     , default='alogtrading' )
    )


class DebugConfig(Config):
    DEBUG = True


# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}
