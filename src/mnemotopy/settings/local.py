# -*- coding: utf-8 -*-

from .base import *

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

ALLOWED_HOSTS = [
    '*',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mnemotopy',
        'USER': 'mnemotopy',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    },
    'slave': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mnemotopy',
        'USER': 'mnemotopy',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


INSTALLED_APPS += (
    'storages',
)

AWS_STORAGE_BUCKET_NAME = 'mnemotopy-files'
AWS_ACCESS_KEY_ID = 'AKIAIJQYOYB5ZNOKKD4Q'
AWS_SECRET_ACCESS_KEY = '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'

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

STATICFILES_LOCATION = 'static'

MEDIAFILES_LOCATION = 'media'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'mnemotopy.storages.MediaStorage'

BROKER_URL = "amqp://mnemotopy:mnemotopy@localhost:5672/mnemotopy"
