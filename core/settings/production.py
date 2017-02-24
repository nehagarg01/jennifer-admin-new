"""
Django settings for core project, on Heroku. For more info, see:
https://github.com/heroku/heroku-django-template

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import os
import dj_database_url
import urlparse


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), '../..'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: change this before deploying to production!
SECRET_KEY = 'i+acxn5(akgsn!sr4^qgf(^m&*@+g1@u^t@=8s@axc41ml*f=s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Application definition

INSTALLED_APPS = (
    # Django modules
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local apps
    'core',
    'authentication',
    'dashboard',
    'vendors',
    'products',
    'schedule',
    'webhooks',
    'series',
    'discount',

    # External apps
    'django_extensions',
    'bootstrap3',
    'localflavor',
    'djcelery',
    'bootstrap_pagination',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.config(),
}
DATABASES['default']['CONN_MAX_AGE'] = 500

redis_url = urlparse.urlparse(os.environ.get('REDIS_URL', ''))
CACHES = {
    "default": {
         "BACKEND": "redis_cache.RedisCache",
         "LOCATION": "{0}:{1}".format(redis_url.hostname, redis_url.port),
        #  "TIMEOUT": None,
         "OPTIONS": {
             "PASSWORD": redis_url.password,
             "DB": 0,
         }
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Update database configuration with $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = os.path.join(PROJECT_ROOT, 'core', 'static/')

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    # os.path.join(PROJECT_ROOT, 'static'),
)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

BOWER_INSTALLED_APPS = (
    'components-font-awesome',
    'metisMenu',
    'animate.css',
    'bootstrap',
    'select2-bootstrap',
    'jquery',
    'jquery-ui',
    'slimScroll',
    'icheck',
    'peity',
    'jquery.sparkline.dist',
    'jquery-nestable',
    'toastr',
    'jquery.parallax',
    'jquery-mousewheel',
    'malihu-custom-scrollbar-plugin',
    'ion-checkradio',
    'OwlCarouselBower',
    'minimalect',
    'bootstrap-touchspin',
    'javascript-equal-height-responsive-rows',
    'scrollme',
    'pace',
    'jquery-migrate',
    'jquery-cycle2',
    'jquery.easing',
    'bootstrap-datepicker',
    'sweetalert',
    'js-cookie',
    'dropzone',
    'Sortable',
    'blueimp-gallery',
    'blueimp-bootstrap-image-gallery',
    'chartjs',
    'underscore',
    'magnific-popup',
    'moment',
    'fullcalendar',
)

LOGIN_REDIRECT_URL = '/dashboard'

# SHOPIFY API
SHOPIFY_API_KEY = os.environ.get('SHOPIFY_API_KEY', '')
SHOPIFY_PASSWORD = os.environ.get('SHOPIFY_PASSWORD', '')
SHOPIFY_SHOP_NAME = os.environ.get('SHOPIFY_SHOP_NAME', '')
SHOPIFY_APP_API_SECRET = os.environ.get('SHOPIFY_APP_API_SECRET', '')

SHOPIFY_URL = "https://%s:%s@%s.myshopify.com/admin" % (
    SHOPIFY_API_KEY, SHOPIFY_PASSWORD, SHOPIFY_SHOP_NAME,)


CELERY_DEFAULT_RATE_LIMIT = 6
from celery.schedules import crontab
CELERYBEAT_SCHEDULE = {
    'run-schedule-of-the-day': {
        'task': 'schedule.tasks.run_schedule',
        'schedule': crontab(hour=0, minute=0),
    },
}

CELERY_TIMEZONE = 'US/Eastern'

BROKER_URL = os.environ.get('REDIS_URL', '')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', '')

GOOGLE_API_KEY = "AIzaSyDdyh07oa5DtA3D48EgVrEd2XGT_VJBI8E"
