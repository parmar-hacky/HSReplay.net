"""
Django settings for hsreplay.net project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.core.urlresolvers import reverse_lazy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'be8^qa&f2fut7_1%q@x2%nkw5u=-r6-rwj8c^+)5m-6e^!zags'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'storages',
    'web',
    'joust',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.twitch',
    'oauth.battlenet',
)

SOCIALACCOUNT_PROVIDERS = {
    "twitch": {"SCOPE": ["user_read"]},
    "battlenet": {"SCOPE": []}
}

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

# The following section based on: https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/

# Uncomment this block to instruct S3 that when it serves objects it can instruct browsers to cache them for a LONG time.
# AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
#     'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
#     'Cache-Control': 'max-age=94608000',
# }


# AWS_IAM_USER = 'arn:aws:iam::272503103573:user/hsreplayarchiveuser'
AWS_STORAGE_BUCKET_NAME = 'replays.hsreplayarchive.org'
AWS_ACCESS_KEY_ID = 'AKIAINP23BGAX74MXI5A'
AWS_SECRET_ACCESS_KEY = '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'
AWS_S3_CALLING_FORMAT = 'boto.s3.connection.OrdinaryCallingFormat'
AWS_S3_CUSTOM_DOMAIN = AWS_STORAGE_BUCKET_NAME
AWS_S3_SECURE_URLS = False

#STATICFILES_LOCATION = 'static'
#STATICFILES_STORAGE = 'config.storage.StaticStorage'
#STATIC_URL = "http://%s/%s/" % (AWS_STORAGE_BUCKET_NAME, STATICFILES_LOCATION)
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_HOST = 'http://static.hsreplay.net' if not DEBUG else ''
STATIC_URL = STATIC_HOST + '/static/'

if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

MEDIAFILES_LOCATION = 'media'
MEDIA_URL = "http://%s/%s/" % (AWS_STORAGE_BUCKET_NAME, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'config.storage.MediaStorage'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hsreplaynet',
        'USER': os.environ.get('HSREPLAYNET_DB_USER', 'root'),
        'PASSWORD': os.environ.get('HSREPLAYNET_DB_PASSWORD', ''),
        'HOST': os.environ.get('HSREPLAYNET_DB_HOST', 'localhost'),
        'PORT': os.environ.get('HSREPLAYNET_DB_PORT', ''),
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

LOGIN_REDIRECT_URL = reverse_lazy('joust_replay_list')
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

SOCIALACCOUNT_ADAPTER = "oauth.battlenet.provider.BattleNetSocialAccountAdapter"

BATTLE_NET_KEY = os.environ.get('BATTLE_NET_KEY', '')
BATTLE_NET_SECRET = os.environ.get('BATTLE_NET_SECRET', '')
