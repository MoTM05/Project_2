from django.core.exceptions import ImproperlyConfigured

import os
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '__debug__')
DEBUG = bool(int(os.environ.get('DJANGO_DEBUG', True)))

if not DEBUG and SECRET_KEY == 'debug':
    raise ImproperlyConfigured("Secret key is not set")

# Allowed hosts
ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'drf_spectacular',
    'apps.authentication'
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'

# List of available databases for project (sqlite for development, postgres for deployment inside Docker)
AVAILABLE_DATABASES = {
    'sqlite': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3'
        }
    },
    'postgres': {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DB'),
            'USER': os.environ.get('POSTGRES_USER'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
            'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
            'PORT': int(os.environ.get('POSTGRES_PORT', 5432))
        }
    }
}

# Selected database
DATABASES = AVAILABLE_DATABASES[os.environ.get('DJANGO_DB_TYPE', 'sqlite')]


# Password validation
AUTH_PASSWORD_VALIDATORS = []
if not DEBUG:
    # Disable password validation for debug mode
    AUTH_PASSWORD_VALIDATORS += [
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
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'api/static/'
STATIC_ROOT = BASE_DIR / 'static'

# Media files
MEDIA_URL = 'api/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging configuration
LOG_DIRECTORY = BASE_DIR / 'logs'
LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {name} : {message}',
            'style': '{',
        }
    },
    'handlers': {
        'file_apps': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOG_DIRECTORY / 'apps.log',
            'formatter': 'verbose'
        },
        'file_django': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOG_DIRECTORY / 'django.log',
            'formatter': 'verbose'
        },
        'console': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'apps': {
            'handlers': ['file_apps', 'console'],
            'level': 'DEBUG',
        },
        'django': {
            'handlers': ['file_django', 'console'],
            'level': 'INFO',
            'propagate': False
        },
        'django.utils.autoreload': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        }
    }
}

# Settings to make Django work correctly with Nginx under HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

# Custom user model
AUTH_USER_MODEL = 'authentication.CustomUser'

# Django REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication'
    ]
}
if DEBUG:
    # Add basic auth for OpenAPI convenience
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += [
        'rest_framework.authentication.BasicAuthentication'
    ]

# dj-rest-auth settings
REST_AUTH = {
    'USE_JWT': True,
    'TOKEN_MODEL': None,
    'SESSION_LOGIN': False
}

# JWT auth settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=6),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=180)
}

# OpenAPI settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'test1 API',
    'VERSION': '1.0.0',
    'SCHEMA_PATH_PREFIX': '/api',
    'COMPONENT_SPLIT_REQUEST': True
}

# CORS settings
_allowed_origins = os.environ.get('DJANGO_CORS_ALLOWED_ORIGINS', '*').split(' ')
if '*' in _allowed_origins:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOWED_ORIGINS = []
    for host in _allowed_origins:
        if host:
            CORS_ALLOWED_ORIGINS.append("http://" + host)  # noqa
            CORS_ALLOWED_ORIGINS.append("https://" + host)
CORS_ALLOW_CREDENTIALS = True
