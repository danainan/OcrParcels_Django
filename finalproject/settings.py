"""
Django settings for finalproject project.

Generated by 'django-admin startproject' using Django 4.1.9.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
import environ
from urllib.parse import urlparse

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = os.path.join(BASE_DIR, 'ocr/media')
MEDIA_PROJECT = os.path.join(BASE_DIR, 'project/media')
NER_ROOT = os.path.join(BASE_DIR, 'ocr/pythainlp')
OCR_ROOT = os.path.join(BASE_DIR, 'ocr/ocrdata')
MODEL_ROOT = os.path.join(BASE_DIR, 'ocr/model')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-@lny6gwv83(&%1=ekfa)=e7)b3!_&t1rkgggpk=#gysr2cwasg"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []




# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "project",
    "ocr",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = "finalproject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR,"templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "finalproject.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

'''
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
'''

MONGODB_URI = 'mongodb+srv://authachaizzz:1234@cluster0.xf2c6og.mongodb.net/?retryWrites=true&w=majority'
MONGODB_NAME = 'finaldatabase'

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'finaldatabase',
        "CLIENT" :{
        'host': 'mongodb+srv://authachaizzz:1234@cluster0.xf2c6og.mongodb.net/?retryWrites=true&w=majority',
            'username': 'authachaizzz',
            'password': '1234'

        }
    }
}

DEFAULT_FILE_STORAGE = 'gridfs_storage.storage.GridFSStorage'
GRIDFS_STORAGE_OPTIONS = {
    'host': 'mongodb+srv://authachaizzz:1234@cluster0.xf2c6og.mongodb.net/?retryWrites=true&w=majority',
    'database': 'finaldatabase',
    'username': 'authachaizzz',
    'password': '1234',
    'collection_name': 'parcel_users',
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "ocr/static/"),
]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# ALLOWED_HOSTS = ['71a1-202-28-68-33.ngrok-free.app']


