"""
Django settings for core_settings project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!4q%5)zsoado=gqe_2trj0=tst%$#@^2%r31#(ypn6mfafxec0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'common',
    'people',
    'permissions',
    'finance',
    'humanresources',
    'research',
    'orders',
    'reimbursements',
    'suppliers',
    'notifications',
    f'frontend',
    'model_extra_fields',

    'orquestra',
    'pyforms_web.web',
    'jfu',
    'sorl.thumbnail',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites'
]

MIDDLEWARE = [
    'pyforms_web.web.middleware.PyFormsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core_settings.urls'

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

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

WSGI_APPLICATION = 'core_settings.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
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


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'static', "img"),
    os.path.join(BASE_DIR,'static', "css"),
    #os.path.join(BASE_DIR,'static', "js"),
)

# ALL AUTH CONFIGURATION
SITE_ID = 1 # Required for allauth module
LOGIN_REDIRECT_URL = '/'
ACCOUNT_SIGNUP_CLOSED = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_SESSION_REMEMBER = True

PROFILE_GUEST = 'PROFILE: Guest'
PROFILE_GROUP_RESPONSIBLE = 'PROFILE: Group responsible'
PROFILE_LAB_MANAGER = 'PROFILE: Lab manager'
PROFILE_ADMIN = 'PROFILE: Admin'
PROFILE_HUMAN_RESOURCES = 'PROFILE: Human resources'
PROFILE_EDIT_BUDGET = 'PROFILE: Edit budget'
PROFILE_PUBLICATIONS_AUDITOR = 'PROFILE: Publications auditor'
PROFILE_OSP = 'PROFILE: OSP collaborator'
PROFILE_SCICOM = 'PROFILE: SCICOM'

PROFILE_LAB_ADMIN = ''

PROFILE_EXPIRING_CONTRACTS_OF_MY_GROUP = 'PROFILE: 60 Days warning: Expiring contracts of my groups'
PROFILE_EXPIRING_CONTRACTS_AND_PAYOUTS = 'PROFILE: 60 Days warning: Expiring contracts and payouts'
PROFILE_MAINTAINERS = 'PROFILE: Maintainers'