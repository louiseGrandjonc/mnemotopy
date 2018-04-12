# -*- coding: utf-8 -*-

from .base import *

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

ALLOWED_HOSTS = [
    '*',
]

DEBUG = True

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
