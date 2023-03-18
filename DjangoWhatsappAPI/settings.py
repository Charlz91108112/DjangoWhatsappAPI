from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zdlifhdhdtjhtfjnj7y86dun7t86876876761f#%5416tjstj5###$Gtgtwhthvrtj@#%^511687'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['localhost','0.0.0.0', '172.31.15.102', 'api.marketeerfront.com', '3.224.88.183']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Created Apps
    'business',
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

ROOT_URLCONF = 'DjangoWhatsappAPI.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'DjangoWhatsappAPI.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'djangowhatsappapi',
        'USER': 'charlz',
        'PASSWORD': 'DROW-ssap10!',
        'HOST': 'localhost',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = '/uploads/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# SMTP Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'email.host'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'hi@email.com'
EMAIL_HOST_PASSWORD = 'password'
DEFAULT_FROM_EMAIL = 'hi@email.com'

# Login details
#LOGIN_REDIRECT_URL = 'dashboard'
#LOGIN_URL = 'login'

# WhatsApp Configuration
WHATSAPP_URL = 'https://graph.facebook.com/v15.0/115728961432587/messages'
WHATSAPP_TOKEN = 'Bearer EAAIFotLuvroBAJsK9TCyIUFz7v8jbvpTXqZCEbZBv0jPz1c0Bu20fPli9A6d3QmZAsdtcEQYm9DtNMMUN3q7VWP8GScYTHZCZC9DLJSnocCV93hSxdz5670s5YXihLzVGHemS3nXkQxOegEA5GMWar9jBfAqVCkP4lFKYCwnuZCRYCDgGxXIS1UPHeG10mj0n5qsfMXtWVQgZDZD'

# Image Upload API
IMAGE_UPLOAD_URL = 'https://api.imgbb.com/1/upload'
IMAGE_UPLOAD_KEY = 'db5a24b27b1a0fc40fe30487c6d37564'

# OpenAi Configuration
OPENAI_API_KEY = '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'
INTERNET_SEARCH_URL = 'https://phind.com/api/search'
INTERNET_SCRAPE_URL = 'https://phind.com/api/tldr'

# Dalle API
DALLE_API = 'https://xipher.onrender.com/api/v1/dalle'
