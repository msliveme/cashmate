import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'f915759255a437fa13a4b08215315f3b91f0c48525a76fbad2e3a1a1f5713f1b03e451842be597e9a07f302605efcfc3c2a6'

DEBUG = False

ALLOWED_HOSTS = ["cashmate.dupno.com", "91.99.167.26", "localhost"]

CSRF_TRUSTED_ORIGINS = ["https://cashmate.dupno.com", "http://cashmate.dupno.com"]

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cashmate_project.urls'

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

WSGI_APPLICATION = 'cashmate_project.wsgi.application'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('DB_NAME', 'cashmate_db'),
#         'USER': os.environ.get('DB_USER', 'cashmate_user'),
#         'PASSWORD': os.environ.get('DB_PASSWORD', '018874Bl'),
#         'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
#         'PORT': os.environ.get('DB_PORT', '5432'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I1N = True

USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = "/var/www/cashmate/staticfiles"

# For production, run: python manage.py collectstatic


LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
JAZZMIN_SETTINGS = {
    "site_title": "CashMate Admin",
    "site_header": "CashMate",
    "site_brand": "CashMate",
    "welcome_sign": "Welcome to the CashMate Admin",
    "copyright": "CashMate Ltd.",
}
