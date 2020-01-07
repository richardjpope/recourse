import os
import json
from datetime import timedelta

class Config(object):
    PROJECT_NAME = 'Report problems online'
    DEBUG = os.environ.get('DEBUG', False)

    PREFERRED_URL_SCHEME = os.environ.get('PREFERRED_URL_SCHEME', 'https')

    MONGODB_HOST = os.environ.get('MONGO_URI', None)
    SECRET_KEY = os.environ.get('SECRET_KEY', None)
    DATABASE_ENCRYPTION_KEY = os.environ.get('DATABASE_ENCRYPTION_KEY', None) # must be 16, 24 or 32 bytes long
    
    CELERY_TIMEZONE = 'UTC'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_REDIS_MAX_CONNECTIONS = 20
    CELERY_BROKER_URL = os.environ.get('REDIS_URL', None)
    CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', None)
   
class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_DB = "recourse_dev"
    SECRET_KEY = 'not-a-secret-not-a-secret-not-a-secret-not-a-secret-not-a-secret-not-a-secret-not-a-secret-'
    DATABASE_ENCRYPTION_KEY = "DO NOT USE THIS KEY XXXXXXXXXXXX" #do not use this in production

    #TWILLIO_SID = os.environ.get('TWILLIO_SID', None)
    #TWILLIO_AUTH_TOKEN = os.environ.get('TWILLIO_AUTH_TOKEN', None)
    #TWILLIO_PHONE_NUMBER = os.environ.get('TWILLIO_PHONE_NUMBER', None)

    CELERY_BROKER_URL='mongodb://localhost:27017/recourse-tasks'
    CELERY_RESULT_BACKEND='mongodb://localhost:27017/recourse-tasks'

class TestingConfig(DevelopmentConfig):
    TESTING = True
    MONGODB_SETTINGS = {'DB': "recourse_test"}
    WTF_CSRF_ENABLED = False
