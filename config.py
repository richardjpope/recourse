import os
import json
from datetime import timedelta

class Config(object):
    PROJECT_NAME = 'Online Resolution Service'
    DEBUG = os.environ.get('DEBUG', False)
    PREFERRED_URL_SCHEME = os.environ.get('PREFERRED_URL_SCHEME', 'https')
    MONGODB_DB = os.environ.get('MONGODB_DB', None)
    MONGODB_HOST = os.environ.get('MONGODB_HOST', None)
    MONGODB_PORT = int(os.environ.get('MONGODB_PORT', 0))
    MONGODB_USERNAME = os.environ.get('MONGODB_USERNAME', None)
    MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD', None)
    MONGODB_HOST = os.environ.get('MONGO_URI', None)
    SECRET_KEY = os.environ.get('SECRET_KEY', None)
    BASIC_AUTH_FORCE = os.environ.get('BASIC_AUTH_FORCE', True)
    BASIC_AUTH_USERNAME = os.environ.get('BASIC_AUTH_USERNAME', None)
    BASIC_AUTH_PASSWORD = os.environ.get('BASIC_AUTH_PASSWORD', None)
  
  
class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_DB = os.environ.get('MONGODB_DB', 'recourse_dev')
    MONGODB_HOST = os.environ.get('MONGODB_HOST', 'localhost')
    MONGODB_PORT = int(os.environ.get('MONGODB_PORT', 27017))
    SECRET_KEY = 'not-a-secret-not-a-secret-not-a-secret-not-a-secret-not-a-secret-not-a-secret-not-a-secret-'
    BASIC_AUTH_FORCE = False

class TestingConfig(DevelopmentConfig):
    TESTING = True
    MONGODB_DB = os.environ.get('MONGODB_DB', 'recourse_test')
    MONGODB_HOST = os.environ.get('MONGODB_HOST', 'localhost')
    MONGODB_PORT = int(os.environ.get('MONGODB_PORT', 27017))
    WTF_CSRF_ENABLED = False
    BASIC_AUTH_FORCE = False
