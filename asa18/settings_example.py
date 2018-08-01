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

import stripe

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'INEEDTOBESET-NICERANDOMSTRINGPLEASE'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['0.0.0.0', 'localhost', 'asa2018.swin.edu.au']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'captcha',
    # 'tinymce',
    # 'sorl.thumbnail',
    # 'mce_filebrowser',
    'colorfield',
    'asa18',
    'django_extensions',
    'ckeditor',
    'ckeditor_uploader',
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
                "asa18.context_processors.asa18_settings.asa18_settings",
            ]
        }
    },
]

ROOT_URLCONF = 'asa18.urls'

WSGI_APPLICATION = 'asa18.wsgi.application'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'database/db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Australia/Melbourne'

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

# CKEdtitor (WYSIWYG text editor)
CKEDITOR_UPLOAD_PATH = 'mce_filebrowser/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-', 'NewPage', 'Preview', '-', ]},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'insert',
             'items': ['Image', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-',
                       'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-',
                       'BidiLtr', 'BidiRtl', 'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',
                'Source',
            ]},
        ],
        'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
        'extraPlugins': ','.join([
            # 'autogrow',
            'dialog',
            'iframe',
        ]),
        'contentsCss': ['/static/sm_asvo/master.css',
                        'https://fonts.googleapis.com/'
                        'icon?family=Material+Icons',
                        'https://fonts.googleapis.com/'
                        'css?family=Open+Sans:400,700,400italic,700italic',
                        'https://fonts.googleapis.com/'
                        'css?family=Carrois+Gothic', ],
        'bodyClass': 'content',
        # 'autoGrow_maxwidth': 1024,
        # 'autoGrow_onStartup': True,
        'width': '100%',
    }
}

# DJANGO_COUNTRIES SETUP
COUNTRIES_FIRST = ["AUS", "NZ", ]

# Stripe payments config
STRIPE_KEY_PUBLISHABLE = 'pk_test_BlT1jN9xqeIU4iVGFflAJZBX'
STRIPE_KEY_SECRET = 'sk_test_ekVIwIRjcFrysFkLMvgguX4e'
STRIPE_STATEMENT_DESCRIPTOR = 'ASA 2018 Meeting'
stripe.api_key = STRIPE_KEY_SECRET

# Mail settings
EMAIL_HOST = 'gpo.swin.edu.au'
# EMAIL_PORT = 465
EMAIL_PORT = 25
# EMAIL_USE_SSL = True
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
# REGISTRATION_EMAIL = 'ASA2018@astro.swin.edu.au'
REGISTRATION_EMAIL = 'kgereb@swin.edu.au'
DEFAULT_FROM_EMAIL = REGISTRATION_EMAIL

# Page display parameters
GLOBAL_PAGE_TITLE = "ASA 2018"
