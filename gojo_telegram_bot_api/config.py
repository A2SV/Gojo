import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    PORT = os.getenv("TELEGRAM_BOT_PORT", 5000)
    TELEGRAM_API = "https://api.telegram.org"
    OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")
    TELEGRAM_CORE_API_HASH = os.getenv("TELEGRAM_CORE_API_HASH")
    TELEGRAM_CORE_API_ID = os.getenv("TELEGRAM_CORE_API_ID")
    
class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True