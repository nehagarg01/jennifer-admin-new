import os
from .production import *

DATABASES = {
    'default': {
        'NAME': 'jennifer',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'jenniferadmin',
        'PASSWORD': 'jennifer-db-letmein'
    },
}

EMAIL_HOST = '127.0.0.1'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 1025
EMAIL_USE_TLS = False


CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'
