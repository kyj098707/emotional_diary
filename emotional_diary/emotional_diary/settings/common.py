import os
from datetime import timedelta
from os.path import abspath, dirname
from pathlib import Path
import configparser
configs = configparser.ConfigParser()
configs.read('./keys.conf', encoding = "utf-8")
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = dirname(dirname(dirname(abspath(__file__))))
# 현재 파일의 절대 경로의 부모,부모,부모 폴더  

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-_jl&pndl)d-3#+ik%nz$2w!9f%s&k$i^ih3*ld8u4bl_+sh)h$"

# SECURITY WARNING: don't run with debug turned on in production!
# LOGIN 관련
DEBUG = True
ALLOWED_HOSTS = ["ec2-15-164-224-122.ap-northeast-2.compute.amazonaws.com"]


## Email 관련

EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_HOST_USER = "apikey"
EMAIL_HOST_PASSWORD = "apo_"
EMAIL_PORT = 587
EMAIL_USE_TLS= True
WELCOME_EMAIL_SENDER = "a036129@aivle.kt.co.kr"
# Application definition

INSTALLED_APPS = [
    # django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    # third apps
    "django_bootstrap5",
    "rest_framework",
    "rest_framework_simplejwt",

    #local apps
    "diaryapp",
    "accounts",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "emotional_diary.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        #CHAGNGED
        "DIRS": [
            os.path.join(BASE_DIR,"__template")
            #os.path.join(BASE_DIR,"__templates")
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

WSGI_APPLICATION = "emotional_diary.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

AUTH_USER_MODEL = "accounts.User"

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True



#CHANGED--->
STATIC_URL = '/static/'

STATIC_DIR = os.path.join(BASE_DIR,'__static')
STATIC_ROOT = os.path.join(BASE_DIR,'__collect_static')
STATICFILES_DIRS = [
    ("static",STATIC_DIR)
]

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
# <--- CHANGED
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INTERNAL_IPS = [
    "127.0.0.1",
]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',],
    "DEFAULT_PERMISSION_CLASSES":[
        'rest_framework.permissions.IsAuthenticated',
],
}


# SIMPLE_JWT 셋팅
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=300),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('Bearer',),
}
