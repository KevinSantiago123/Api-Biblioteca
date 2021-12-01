""" Django production settings."""

#Settings Base
from library_config.settings.base import *

DEBUG = False

# Hosts appengine
ALLOWED_HOSTS = ['library-backend-333617.ue.r.appspot.com']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'library-backend-333617:us-central1:db-library',
        'NAME': 'library_prod',
        'USER': secret.get('DB_USER_PROD', None),
        'PASSWORD': secret.get('DB_PSW_PROD', None),
    }
}
