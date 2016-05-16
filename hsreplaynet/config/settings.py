"""
Django settings for hsreplay.net project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from datetime import datetime
from django.core.urlresolvers import reverse_lazy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IS_RUNNING_AS_LAMBDA = bool(os.environ.get('IS_RUNNING_AS_LAMBDA', ''))


FIXTURE_DIRS = (os.path.join(BASE_DIR, 'test', 'fixtures'),)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'be8^qa&f2fut7_1%q@x2%nkw5u=-r6-rwj8c^+)5m-6e^!zags'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
if IS_RUNNING_AS_LAMBDA:
    DEBUG = False

ALLOWED_HOSTS = []


if not IS_RUNNING_AS_LAMBDA:
    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',
        'web',
        'joust',
        'cards',
        'lambdas',
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'allauth_battlenet',
    )

    SOCIALACCOUNT_PROVIDERS = {
        "battlenet": {"SCOPE": []}
    }

else:
    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',
        'web',
        'joust',
        'cards',
        'lambdas',
    )


TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.gzip.GZipMiddleware',
)

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

S3_RAW_LOG_STORAGE_BUCKET = os.environ.get('S3_RAW_LOG_STORAGE_BUCKET', 'test.raw.replaystorage.hsreplay.net')
S3_REPLAY_STORAGE_BUCKET = os.environ.get('S3_REPLAY_STORAGE_BUCKET', 'test.replaystorage.hsreplay.net')
AWS_STORAGE_BUCKET_NAME = S3_REPLAY_STORAGE_BUCKET

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_USE_SSL = False

AWS_IS_GZIPPED = True
GZIP_CONTENT_TYPES = (
    'text/xml',
    'text/plain',
    'application/xml',
    'application/octet-stream',
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

if DEBUG:
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    STATIC_HOST = ""
else:
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    STATICFILES_STORAGE = "whitenoise.django.GzipManifestStaticFilesStorage"
    STATIC_HOST = "//static.hsreplay.net"
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = STATIC_HOST + '/static/'



# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "hsreplay.db"),
            "USER": "",
            "PASSWORD": "",
            "HOST": "",
            "PORT": "",
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'hsreplaynet',
            'USER': os.environ.get('HSREPLAYNET_DB_USER', 'django'),
            'PASSWORD': os.environ.get('HSREPLAYNET_DB_PASSWORD', 'db_pass'),
            'HOST': os.environ.get('HSREPLAYNET_DB_HOST', 'localhost'),
            'PORT': os.environ.get('HSREPLAYNET_DB_PORT', ''),
        }
    }

if not IS_RUNNING_AS_LAMBDA:
    # When we are running on Lambda the logging is configured by the runtime to write to CloudWatch so this is not needed.
    LOG_ROOT_DIR = os.environ.get('DJANGO_LOG_ROOT_DIR', os.path.abspath(os.path.join(BASE_DIR, '../log')))

    if not os.path.exists(LOG_ROOT_DIR):
        os.mkdir(LOG_ROOT_DIR)

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                'datefmt' : "%d/%b/%Y %H:%M:%S"
            },
        },
        'handlers': {
            'joust': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(LOG_ROOT_DIR, 'joust.log'),
                'maxBytes': 5242880,
                'backupCount': 5,
                'formatter': 'verbose'
            },
            'timing': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(LOG_ROOT_DIR, 'timing.log'),
                'maxBytes': 5242880,
                'backupCount': 5,
                'formatter': 'verbose'
            },
            'web': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(LOG_ROOT_DIR, 'web.log'),
                'maxBytes': 5242880,
                'backupCount': 5,
                'formatter': 'verbose'
            },
            'django_file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(LOG_ROOT_DIR, 'django.log'),
                'maxBytes': 5242880,
                'backupCount': 5,
                'formatter': 'verbose'
            },
            'error_file': {
                'level': 'ERROR',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(LOG_ROOT_DIR, 'error.log'),
                'maxBytes': 5242880,
                'backupCount': 5,
                'formatter': 'verbose'
            },
            'battlenet': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(LOG_ROOT_DIR, 'battlenet.log'),
                'maxBytes': 5242880,
                'backupCount': 5,
                'formatter': 'verbose'
            },
        },
        'loggers': {
            'django': {
                'handlers':['django_file', 'error_file'],
                'propagate': True,
                'level':'INFO',
            },
            'TIMING': {
                'handlers':['timing'],
                'propagate': True,
                'level':'INFO',
            },
            'joust': {
                'handlers': ['joust', 'error_file'],
                'propagate': False,
                'level': 'DEBUG',
            },
            'web': {
                'handlers': ['web', 'error_file'],
                'propagate': False,
                'level': 'DEBUG',
            },
            'allauth_battlenet': {
                'handlers': ['battlenet', 'error_file'],
                'propagate': False,
                'level': 'DEBUG',
            },
        }
    }



# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

LOGIN_REDIRECT_URL = reverse_lazy("my_replays")
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http" if DEBUG else "https"

SOCIALACCOUNT_ADAPTER = "allauth_battlenet.provider.BattleNetSocialAccountAdapter"

API_KEY_HEADER = 'x-hsreplay-api-key'
UPLOAD_TOKEN_HEADER = 'x-hsreplay-upload-token'
