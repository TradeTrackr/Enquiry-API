import os

def convert_to_bool(value):
    if value == "True":
        return True
    elif value == "False":
        return False

APP_NAME = os.environ['APP_NAME']
APM_ENABLED = convert_to_bool(os.environ['APM_ENABLED'])
ACCOUNT_API_ENDPOINT = os.environ['ACCOUNT_API_ENDPOINT']

SQLALCHEMY_MIGRATE_REPO = os.environ['SQLALCHEMY_MIGRATE_REPO']

SQLALCHEMY_USER = os.environ['SQLALCHEMY_USER']
SQLALCHEMY_PASSWORD = os.environ['SQLALCHEMY_PASSWORD']
SQLALCHEMY_HOST = os.environ['SQLALCHEMY_HOST']
SQLALCHEMY_PORT = os.environ['SQLALCHEMY_PORT']
SQLALCHEMY_DB = os.environ['SQLALCHEMY_DB']
postgresql_string = 'postgresql://{}:{}@{}:{}/{}'
SQLALCHEMY_DATABASE_URI = postgresql_string.format(SQLALCHEMY_USER, SQLALCHEMY_PASSWORD, SQLALCHEMY_HOST, SQLALCHEMY_PORT, SQLALCHEMY_DB)

BUCKET_ID = os.environ['BUCKET_ID']
BUCKET_NAME = os.environ['BUCKET_NAME']
aws_access_key_id = os.environ['ACCESS_KEY']
aws_secret_access_key = os.environ['aws_SECRET_KEY']
aws_access_key_id_LIMITED = os.environ['ACCESS_KEY_LIMITED']
aws_secret_access_key_LIMITED = os.environ['aws_SECRET_KEY_LIMITED']
SQS_QUEUE_NAME = os.environ['SQS_QUEUE_NAME']


SET_POOL = os.environ['SET_POOL']

FLASK_LOG_LEVEL = os.environ['FLASK_LOG_LEVEL']

LOGCONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            '()': 'text_message_api.extensions.JsonFormatter'
        },
        'audit': {
            '()': 'text_message_api.extensions.JsonAuditFormatter'
        }
    },
    'filters': {
        'contextual': {
            '()': 'text_message_api.extensions.ContextualFilter'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'filters': ['contextual'],
            'stream': 'ext://sys.stdout'
        },
        'audit_console': {
            'class': 'logging.StreamHandler',
            'formatter': 'audit',
            'filters': ['contextual'],
            'stream': 'ext://sys.stdout'
        }
    },
    'loggers': {
        'application': {
            'handlers': ['console'],
            'level': FLASK_LOG_LEVEL
        },
        'audit': {
            'handlers': ['audit_console'],
            'level': 'INFO'
        }
    }
}
