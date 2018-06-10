"""
Base settings for Political Sisterhood project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
import environ
from os.path import abspath, basename, dirname, join

ROOT_DIR = environ.Path(__file__) - 3  # (political_sisterhood/config/settings/base.py - 3 = political_sisterhood/)
APPS_DIR = ROOT_DIR.path('political_sisterhood')
# PATH CONFIGURATION
# Absolute filesystem path to the config directory:
CONFIG_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the project directory:
PROJECT_ROOT = dirname(CONFIG_ROOT)

# Project name:
PROJECT_NAME = basename(PROJECT_ROOT).capitalize()

# Absolute filesystem path to the django repo directory:
DJANGO_ROOT = PROJECT_ROOT

# Load operating system environment variables and then prepare to use them
env = environ.Env()

# .env file, should load only in development environment
READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)

if READ_DOT_ENV_FILE:
    # Operating System Environment variables have precedence over variables defined in the .env file,
    # that is to say variables from the .env files will only be used if not defined
    # as environment variables.
    env_file = str(ROOT_DIR.path('.env'))
    print('Loading : {}'.format(env_file))
    env.read_env(env_file)
    print('The .env file has been loaded. See base.py for more information')

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Useful template tags:
    # 'django.contrib.humanize',
    'dal',
    'dal_select2',
    # Admin
    'django.contrib.admin',
]
THIRD_PARTY_APPS = [
    'crispy_forms',  # Form layouts
    'allauth',  # registration
    'allauth.account',  # registration
    'allauth.socialaccount',  # registration
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.linkedin_oauth2',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.google',
    'ckeditor', #ckeditor
    'ckeditor_uploader', #ckeditor upload
    'mptt',
    'haystack',
    'betterforms',
    'django_extensions',
    'djstripe',
]


# Apps specific for this project go here.
LOCAL_APPS = [
    # custom users app
    'political_sisterhood.users.apps.UsersConfig',
    # Your stuff: custom apps go here
    'political_sisterhood.candidate',
    'political_sisterhood.issue',
    'political_sisterhood.news',
    'political_sisterhood.races',
    'political_sisterhood.jobs',
    'political_sisterhood.resources',
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# MIGRATIONS CONFIGURATION
# ------------------------------------------------------------------------------
MIGRATION_MODULES = {
    'sites': 'political_sisterhood.contrib.sites.migrations'
}

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('DJANGO_DEBUG', False)

# FIXTURE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    str(APPS_DIR.path('fixtures')),
)

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [
    ("""Christopher Mallon""", 'me@christophermallon.com'),
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
# Uses django-environ to accept uri format
# See: https://django-environ.readthedocs.io/en/latest/#supported-types
DATABASES = {
    'default': env.db('DATABASE_URL', default='postgres:///political_sisterhood'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True


# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'OPTIONS': {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                # Your stuff: custom template context processors go here
                'political_sisterhood.candidate.context_processors.candidates',
            ],
        },
    },
]

# See: http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR('staticfiles'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    str(APPS_DIR.path('static')),
]

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR('media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'

# PASSWORD STORAGE SETTINGS
# ------------------------------------------------------------------------------
# See https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]

# PASSWORD VALIDATION
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
# ------------------------------------------------------------------------------

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

# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Some really nice defaults
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

ACCOUNT_ALLOW_REGISTRATION = env.bool('DJANGO_ACCOUNT_ALLOW_REGISTRATION', True)
ACCOUNT_ADAPTER = 'political_sisterhood.users.adapters.AccountAdapter'
SOCIALACCOUNT_ADAPTER = 'political_sisterhood.users.adapters.SocialAccountAdapter'

# Custom user app defaults
# Select the correct user model
AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = 'users:detail'
LOGIN_URL = 'account_login'

# SLUGLIFIER
AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'

########## CELERY
INSTALLED_APPS += ['political_sisterhood.taskapp.celery.CeleryConfig']
CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='django://')
if CELERY_BROKER_URL == 'django://':
    CELERY_RESULT_BACKEND = 'redis://'
else:
    CELERY_RESULT_BACKEND = CELERY_BROKER_URL
########## END CELERY
# django-compressor
# ------------------------------------------------------------------------------
INSTALLED_APPS += ['compressor']
STATICFILES_FINDERS += ['compressor.finders.CompressorFinder']

# Location of root django.contrib.admin URL, use {% url 'admin:index' %}
ADMIN_URL = r'^admin/'

# Your common stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------

########## LOGGING CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'production_only': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'development_only': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)-8s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%m/%d/%Y %H:%M:%S',
        },
        'simple': {
            'format': '%(levelname)-8s [%(name)s:%(lineno)s] %(message)s',
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'default': {
            'level': 'DEBUG',
            'class': 'config.lib.colorstreamhandler.ColorStreamHandler',
        },
        'console_dev': {
            'level': 'DEBUG',
            'filters': ['development_only'],
            'class': 'config.lib.colorstreamhandler.ColorStreamHandler',
            'formatter': 'simple',
        },
        'console_prod': {
            'level': 'INFO',
            'filters': ['production_only'],
            'class': 'config.lib.colorstreamhandler.ColorStreamHandler',
            'formatter': 'simple',
        },
        'file_log': {
            'level': 'DEBUG',
            'filters': ['development_only'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': join(DJANGO_ROOT, 'logs/log.log'),
            'maxBytes': 1024 * 1024,
            'backupCount': 3,
            'formatter': 'verbose',
        },
        'file_sql': {
            'level': 'DEBUG',
            'filters': ['development_only'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': join(DJANGO_ROOT, 'logs/sql.log'),
            'maxBytes': 1024 * 1024,
            'backupCount': 3,
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['production_only'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
    },
    # Catch-all modules that use logging
    # Writes to console and file on development, only to console on production
    'root': {
        'handlers': ['console_dev', 'console_prod', 'file_log'],
        'level': 'DEBUG',
    },
    'loggers': {
        # Write all SQL queries to a file
        'django.db.backends': {
            'handlers': ['file_sql'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # Email admins when 500 error occurs
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}
# END LOGGING CONFIGURATION

# CKEDITOR CONFIGURATION
CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
        ],
    }
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch2_backend.Elasticsearch2SearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}

# ALLAUTH CONFIGURATION
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
SOCIALACCOUNT_AUTO_SIGNUP = False
ACCOUNT_SIGNUP_FORM_CLASS = 'political_sisterhood.users.forms.SignupForm'

DJSTRIPE_SUBSCRIBER_MODEL  = 'users.User'
STRIPE_LIVE_PUBLIC_KEY = env("STRIPE_LIVE_PUBLIC_KEY")
STRIPE_LIVE_SECRET_KEY = env("STRIPE_LIVE_SECRET_KEY")
STRIPE_TEST_PUBLIC_KEY = env("STRIPE_TEST_PUBLIC_KEY")
STRIPE_TEST_SECRET_KEY = env("STRIPE_TEST_SECRET_KEY")
STRIPE_LIVE_MODE = env.bool('STRIPE_MODE', False)
