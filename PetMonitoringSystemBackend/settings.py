"""
Django settings for PetMonitoringSystemBackend project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path
import logstash

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', '123456')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', True)

ALLOWED_HOSTS = ["127.0.0.1", "*"]
# CORS Settings
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]
CORS_ALLOWED_HEADERS = "*"
CORS_ORIGIN_ALLOW_METHODS = "*"
CORS_ORIGIN_WHITELIST = [
    "http://localhost:8080",
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_elasticsearch_dsl',
    'corsheaders',
    'django_redis',
    'drf_yasg',
    'channels',

    'django_forest',

    'health_check',  # required
    'health_check.db',  # stock Django health checkers
    'health_check.cache',
    'health_check.storage',
    'health_check.contrib.migrations',
    'health_check.contrib.rabbitmq',  # requires RabbitMQ broker
    'health_check.contrib.redis',  # requires Redis

    'api',
    'ws',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'PetMonitoringSystemBackend.urls'

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

WSGI_APPLICATION = 'PetMonitoringSystemBackend.wsgi.application'
ASGI_APPLICATION = 'PetMonitoringSystemBackend.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [f"redis://{os.getenv('REDIS_HOST','127.0.0.1')}:{os.getenv('REDIS_PORT',6379)}/2"],
        },
    },
    "memory": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    },
}
# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("POSTGRES_DB", "PET"),
        'USER': os.getenv("POSTGRES_USER", "test"),
        'PASSWORD': os.getenv("POSTGRES_PASSWORD", "123456"),
        'HOST': os.getenv("POSTGRES_DB_URL", "127.0.0.1"),
        'PORT': '5432'
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = 'zh-TW'
TIME_ZONE = 'Asia/Taipei'
USE_I18N = True
USE_L10N = True
USE_TZ = True
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Elasticsearch DSL Configuration
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': os.getenv("ELASTICSEARCH_ENDPOINT", "127.0.0.1:9200")
    },
}

# RabbitMQ Config
RABBITMQ_CONFIG = {
    "enable": os.getenv("RABBITMQ_ENABLE", False),
    "username": os.getenv("RABBITMQ_USERNAME", "guest"),
    "password": os.getenv("RABBITMQ_PASSWORD", "guest"),
    "serverip": os.getenv("RABBITMQ_SERVER_IP", "127.0.0.1"),
    "port": os.getenv("RABBITMQ_PORT", "5672"),
    "vhost": os.getenv("RABBITMQ_VIRTUAL_HOST", "/")
}
BROKER_URL = f'amqp://{RABBITMQ_CONFIG["username"]}:{RABBITMQ_CONFIG["password"]}@{RABBITMQ_CONFIG["serverip"]}:{RABBITMQ_CONFIG["port"]}{RABBITMQ_CONFIG["vhost"]}'

# chatBot Config
CHATGPT_CONFIG = {
    "enable": os.getenv("CHATGPT_ENABLE", False),
    "api_key": os.getenv("CHATGPT_APIKEY", None)
}

# Redis Cache

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{os.getenv('REDIS_HOST','127.0.0.1')}:{os.getenv('REDIS_PORT', ':6379')}/1",
        # 1 is Database Number
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        'KEY_PREFIX': 'Cache'
    },
}
REDIS_URL = CACHES["default"]["LOCATION"]

# Django Forest admin Setting
FOREST = {
    'FOREST_URL': os.getenv("FOREST_URL", 'https://api.forestadmin.com'),
    'FOREST_ENV_SECRET': os.getenv("FOREST_ENV_SECRET", None),
    'FOREST_AUTH_SECRET': os.getenv("FOREST_AUTH_SECRET", None)
}
APPEND_SLASH = False

# Logstash Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'logstash': {
            'level': 'DEBUG',
            'class': 'logstash.TCPLogstashHandler',
            'host': os.getenv("LOGSTASH_SERVER_IP", 'localhost'),
            'port': os.getenv("LOGSTASH_PORT", 5000),  # Default value: 5959
            'version': 1,
            # Version of logstash event schema. Default value: 0 (for backward compatibility of the library)
            'message_type': 'django',  # 'type' field in logstash message. Default value: 'logstash'.
            'fqdn': False,  # Fully qualified domain name. Default value: false.
            'tags': ['django.request'],  # list of tags. Default: None.
        }
    },
    'root': {
        'handlers': ['console', 'logstash'],
        'level': 'DEBUG',
    },
}
