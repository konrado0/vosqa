# encoding:utf-8
import os.path

SITE_SRC_ROOT = os.path.dirname(__file__)
LOG_FILENAME = 'django.osqa.log'
LOGGING = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(pathname)s TIME: %(asctime)s MSG: %(filename)s:%(funcName)s:%(lineno)d %(message)s',
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': os.path.join(SITE_SRC_ROOT, 'log', LOG_FILENAME),
        },
    },
    'loggers' : {
        # ensure that all log entries are propagated to root
        'django': { 'propagate': True },
        'django.request': { 'propagate': True },
        'django.security': { 'propagate': True },
        'py.warnings': { 'propagate': True },
    },
    'root': {
        'handlers': ['file'],
        'level': 'DEBUG',
    },
}

#ADMINS and MANAGERS
ADMINS = ()
MANAGERS = ADMINS

DEBUG = True
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False
}
TEMPLATE_DEBUG = DEBUG
INTERNAL_IPS = ('127.0.0.1',)
ALLOWED_HOSTS = ('127.0.0.1',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'osqa',
        'USER': 'dressbook',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'ATOMIC_REQUEST': True,
    }
}
# Lets not have a cache folder inside repository
# Cache backend settings moved down to local.py
# CACHE_BACKEND = 'file://%s' % os.path.join(r'/tmp/osqa', 'cache').replace('\\', '/')
# CACHE_BACKEND = 'file://%s' % os.path.join(os.path.dirname(__file__),'cache').replace('\\','/')
# CACHE_BACKEND = 'dummy://'
# CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# This should be equal to your domain name, plus the web application context.
# This shouldn't be followed by a trailing slash.
# I.e., http://www.yoursite.com or http://www.hostedsite.com/yourhostapp
APP_URL = 'http://127.0.0.1:8000'

#LOCALIZATIONS
TIME_ZONE = 'Europe/Warsaw'

#OTHER SETTINGS

USE_I18N = True
LANGUAGE_CODE = 'en'

DJANGO_VERSION = 1.7
OSQA_DEFAULT_SKIN = 'default'

DISABLED_MODULES = ['books', 'recaptcha', 'openidauth', 'project_badges', 'sphinxfulltext',]
