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
SHOPIFY_API_KEY = '72ab69d971a880724b46502f9e7fa0b8'
SHOPIFY_PASSWORD = '0aaadb88f5d53f8683e5dd1344c02f42'
SHOPIFY_SHOP_NAME = "test-flash"
SHOPIFY_APP_API_SECRET = "1d2a706e4a9fd74cf7e561f4d4f59428314ab2afeda552ba0e2e1086c0ccd7ff"

SHOPIFY_URL = "https://%s:%s@%s.myshopify.com/admin" % (
    SHOPIFY_API_KEY, SHOPIFY_PASSWORD, SHOPIFY_SHOP_NAME,)
