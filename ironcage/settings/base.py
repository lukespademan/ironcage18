"""
Django settings for ironcage project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

import dj_database_url
import structlog

from ironcage import structlog_setup

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Used for distinguishing settings that are unset in production.
ENVVAR_SENTINAL = 'not-for-production'
# Settings that must be set in production.
ENVVAR_WATCHED = [
    'SECRET_KEY',
]


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', ENVVAR_SENTINAL)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


# Application definition

INSTALLED_APPS = [
    'accounts',
    'ironcage',

    'bootstrap3',
    'django_slack',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ironcage.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'ironcage.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(default='postgres://localhost/ironcage')
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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


# Custom User model

AUTH_USER_MODEL = 'accounts.User'


# Post-login/out URLs

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'colored': {
            '()': structlog.stdlib.ProcessorFormatter,
            'processor': structlog.dev.ConsoleRenderer(colors=True),
            'foreign_pre_chain': structlog_setup.pre_chain,
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'colored',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'slack': {
            'level': 'ERROR',
            'class': 'django_slack.log.SlackExceptionHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins', 'slack'],
            'level': os.getenv('LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        '': {
            'handlers': ['console'],
            'level': os.getenv('LOG_LEVEL', 'INFO'),
        },
    },
}


# Slack

SLACK_TOKEN = os.environ.get('SLACK_TOKEN', ENVVAR_SENTINAL)
SLACK_CHANNEL = '#ironcage-logs'
SLACK_USERNAME = 'ironcage-log-bot'


# Admins for mailing errors to

ADMINS = [['-', email_addr] for email_addr in os.environ.get('ADMINS', '').split(',')]

# Email address to send mail from

DEFAULT_FROM_EMAIL = 'PyCon UK 2018 <noreply@pyconuk.org>'
SERVER_EMAIL = 'PyCon UK 2018 <noreply@pyconuk.org>'
EMAIL_FROM_ADDR = 'PyCon UK 2018 <noreply@pyconuk.org>'
EMAIL_REPLY_TO_ADDR = 'PyCon UK 2018 <pyconuk-committee@uk.python.org>'
