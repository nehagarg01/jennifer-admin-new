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


# SHOPIFY API
SHOPIFY_API_KEY = '085edcda46fe44fb992d229c8b4accd3'
SHOPIFY_PASSWORD = 'ef2db6b148a5433c5482d4502defa102'
SHOPIFY_SHOP_NAME = "jennifer-development"
SHOPIFY_APP_API_SECRET = "289dd0854e0d5e3d031b394d16fba24da6b66a0845123d03b9bfcf3737343ef5"

SHOPIFY_URL = "https://%s:%s@%s.myshopify.com/admin" % (
    SHOPIFY_API_KEY, SHOPIFY_PASSWORD, SHOPIFY_SHOP_NAME,)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
