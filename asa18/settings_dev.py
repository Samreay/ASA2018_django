"""
Django settings for asa18 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'llk5rhxp6^*j^0^!c84u(utby+6^2$-8*+pm6i36fn(n#^5d$*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '0.0.0.0']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'captcha',
    'tinymce',
    'sorl.thumbnail',
    'mce_filebrowser',
    'colorfield',
    'asa18',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS' : {
            'context_processors': [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.request",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ]
        }
    },
]
# TEMPLATE_CONTEXT_PROCESSORS = (
#     "django.contrib.auth.context_processors.auth",
#     "django.template.context_processors.debug",
#     "django.template.context_processors.i18n",
#     "django.template.context_processors.media",
#     "django.template.context_processors.static",
#     "django.template.context_processors.request",
#     "django.template.context_processors.tz",
#     "django.contrib.messages.context_processors.messages",
#     )

ROOT_URLCONF = 'asa18.urls_dev'

WSGI_APPLICATION = 'asa18.wsgi.application'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Australia/Sydney'

USE_I18N = True

USE_L10N = True

USE_TZ = True

APPEND_SLASH = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# TinyMCE setup
TINYMCE_DEFAULT_CONFIG = {
    'theme' : 'advanced',
    'relative_urls': False,
    'file_browser_callback': 'mce_filebrowser',
    'resize': True,
    'theme_advanced_resizing': True,
    'width': 600,
    'height': 600,
}

# DJANGO_COUNTRIES SETUP
COUNTRIES_FIRST = ["AUS", "NZ", ]

# OneStop config
ONESTOP_TRAN_TYPE = '483'
ONESTOP_GLCODE = 'R.35250.ASA.9280'
ONESTOP_STOREID = 'ASA2017'
ONESTOP_PAYMENT_URL = 'fake.test.payment/'
ONESTOP_SECRET_HASH = 'rwar'
ONESTOP_SECRET_HASH_KEY = 'rxCgXTtcHG5uy34r'

# Mail settings
EMAIL_HOST = 'mso.anu.edu.au'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'skymap'
EMAIL_HOST_PASSWORD = 'Blu8*1=1'
# EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
REGISTRATION_EMAIL = 'ASA2018@astro.swin.edu.au'

# Page display parameters
GLOBAL_PAGE_TITLE = "ASA 2018"
