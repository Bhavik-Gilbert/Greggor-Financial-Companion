"""
Django settings for gfc project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
from django.contrib.messages import constants as messages
from typing import Any, Union, Literal
from dotenv import load_dotenv

# Load environment data
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR: Path = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-)2rxjsa3d&2d83qxnyjyca(d(kl=tt6g*h&*et!-u$fa-w94_j'")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG: bool = True  # TODO: set false before submission

ALLOWED_HOSTS: list[str] = ["127.0.0.1", "localhost"]


# Application definition

INSTALLED_APPS: list[str] = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'financial_companion',
    'widget_tweaks',
    'django_q',
    'django_cleanup.apps.CleanupConfig',
]

X_FRAME_OPTIONS: str = 'SAMEORIGIN'

MIDDLEWARE: list[str] = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF: str = 'gfc.urls'

TEMPLATES: list[dict[str, Any]] = [
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

WSGI_APPLICATION: str = 'gfc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES: dict[dict[str, Any]] = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

FIXTURE_DIRS: list[Path] = [
    os.path.join(
        BASE_DIR,
        "financial_companion/tests/fixtures")]
TEXT_DATA_DIRS: dict[str, Path] = {
    "financial_companion": os.path.join(BASE_DIR, "financial_companion/data")
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS: list[dict[str, str]] = [
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

# Message tags enum
MESSAGE_TAGS: dict[int, str] = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Session timeout information
SESSION_EXPIRE_SECONDS: int = 3600  # 1 hour
SESSION_EXPIRE_AFTER_LAST_ACTIVITY: bool = True

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE: str = 'en-us'

TIME_ZONE: str = 'UTC'

USE_I18N: bool = True

USE_TZ: bool = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL: str = '/static/'
STATICFILES_DIRS: Path = [os.path.join(BASE_DIR, "static")]


# Media files
MEDIA_URL: str = '/media/'
MEDIA_ROOT: Path = os.path.join(BASE_DIR, 'media')

# File upload handler
FILE_UPLOAD_HANDLERS: list[str] = [
    'django.core.files.uploadhandler.TemporaryFileUploadHandler']


# User model for authentication and login purposes
AUTH_USER_MODEL: str = 'financial_companion.User'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# URL to redirect to and from on protected pages
# TODO: Change pages when made
LOGIN_URL: str = "log_in"
LOGGED_IN_URL: str = "dashboard"

# Number of items per pagniated page
NUMBER_OF_ITEMS_PER_PAGE: int = 10

# salt for secure string
SALT_KEY = os.environ.get("SECURE_STRING_SALT", "temporarysalt")

# Default language for Faker
FAKER_LOCALE: str = "en_GB"

# Information for email password reset
EMAIL_BACKEND: str = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST: str = "smtp.gmail.com"
EMAIL_HOST_USER: str = "gfcsystem10@gmail.com"
EMAIL_HOST_PASSWORD: str = os.environ.get(
    "EMAIL_PASSWORD_KEY")
EMAIL_PORT: int = 587
EMAIL_USE_TLS: bool = True
EMAIL_USE_SSL: bool = False

Q_CLUSTER: dict[str, Any] = {
    'name': "financial_companion_schedulers",
    'retry': 60,
    'timeout': 30,
    'workers': 4,
    'orm': 'default'
}

# Site url
SITE_URL_SPENDING_PAGE: str = "http://localhost:8000/spending_summary"
