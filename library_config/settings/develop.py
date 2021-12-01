""" Django local settings."""

#Settings Base
from library_config.settings.base import *

DEBUG = True

# Hosts
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1'
    ]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': '34.136.171.146',
        'PORT': '5432',
        'NAME': 'library_dev',
        'USER': secret.get('DB_USER_DEV', None),
        'PASSWORD': secret.get('DB_PSW_DEV', None),
    }
}
