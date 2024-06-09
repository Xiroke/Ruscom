"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from config import (POSTGRESQL_ENGINE, 
                    POSTGRESQL_NAME, 
                    POSTGRESQL_USER, 
                    POSTGRESQL_PASSWORD, 
                    POSTGRESQL_HOST, 
                    POSTGRESQL_PORT,
                    EMAIL_HOST_PASSWORD,)

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
  "home",
  "search",
  "wagtail.contrib.forms",
  "wagtail.contrib.redirects",
  "wagtail.embeds",
  "wagtail.sites",
  "wagtail.users",
  "wagtail.snippets",
  "wagtail.documents",
  "wagtail.images",
  "wagtail.search",
  "wagtail.admin",
  "wagtail",
  "modelcluster",
  "taggit",
  "django.contrib.admin",
  "django.contrib.auth",
  "django.contrib.contenttypes",
  "django.contrib.sessions",
  "django.contrib.messages",
  "django.contrib.staticfiles",

  'django_email_verification',
  
  'polymorphic',

  'index',
]

MIDDLEWARE = [
  "django.contrib.sessions.middleware.SessionMiddleware",
  "django.middleware.common.CommonMiddleware",
  "django.middleware.csrf.CsrfViewMiddleware",
  "django.contrib.auth.middleware.AuthenticationMiddleware",
  "django.contrib.messages.middleware.MessageMiddleware",
  "django.middleware.clickjacking.XFrameOptionsMiddleware",
  "django.middleware.security.SecurityMiddleware",
  "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = "mysite.urls"

TEMPLATES = [
  {
      "BACKEND": "django.template.backends.django.DjangoTemplates",
      "DIRS": [
          os.path.join(PROJECT_DIR, "templates"),
      ],
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

WSGI_APPLICATION = "mysite.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


# DATABASES = {
#   "default": {
#       "ENGINE": "django.db.backends.sqlite3",
#       "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
#   }
# }

DATABASES = {
  "default": {
      "ENGINE": POSTGRESQL_ENGINE,
      "NAME": POSTGRESQL_NAME,
      "USER": POSTGRESQL_USER,
      "PASSWORD": POSTGRESQL_PASSWORD,
      "HOST": "POSTGRESQL_HOST",
      "PORT": POSTGRESQL_PORT,
  }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
  {
      "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
  },
  {
      "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
  },
  {
      "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
  },
  {
      "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
  },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATICFILES_FINDERS = [
  "django.contrib.staticfiles.finders.FileSystemFinder",
  "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
  os.path.join(PROJECT_DIR, "static"),
]

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Default storage settings, with the staticfiles storage updated.
# See https://docs.djangoproject.com/en/5.0/ref/settings/#std-setting-STORAGES
STORAGES = {
  "default": {
      "BACKEND": "django.core.files.storage.FileSystemStorage",
  },
  # ManifestStaticFilesStorage is recommended in production, to prevent
  # outdated JavaScript / CSS assets being served from cache
  # (e.g. after a Wagtail upgrade).
  # See https://docs.djangoproject.com/en/5.0/ref/contrib/staticfiles/#manifeststaticfilesstorage
  "staticfiles": {
      "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
  },
}


# Wagtail settings

WAGTAIL_SITE_NAME = "mysite"

# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
  "default": {
      "BACKEND": "wagtail.search.backends.database",
  }
}

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = "http://example.com"

AUTH_USER_MODEL = 'index.User'


# For Email Verification
def verified_callback(user):
  user.is_active = True




EMAIL_MAIL_CALLBACK = verified_callback
EMAIL_VERIFIED_CALLBACK = verified_callback
EMAIL_FROM_ADDRESS = 'ruscomsite@gmail.com'
EMAIL_MAIL_SUBJECT = 'Confirm your email {{ user.username }}'
EMAIL_MAIL_HTML = 'index/mail_body.html'
EMAIL_MAIL_PLAIN = 'index/mail_body.txt'
EMAIL_MAIL_TOKEN_LIFE = 60 * 60
EMAIL_MAIL_PAGE_TEMPLATE = 'index/confirm_template.html'
EMAIL_PAGE_DOMAIN = 'http://127.0.0.1:8000/' # Host
# EMAIL_MULTI_USER = True  # optional (defaults to False)

# For Django Email Backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ruscomsite@gmail.com'
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'ruscomsite@gmail.com'
SERVER_EMAIL = 'ruscomsite@gmail.com'

