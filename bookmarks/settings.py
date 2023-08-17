"""
Django settings for bookmarks project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os.path
from pathlib import Path
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-jhd8%egj)5&it9++8woc2$&bpq!v#)y7*zhk&!h7ged&x%4j!p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['mysite.com', 'localhost', '127.0.0.1']
# Django controls the hosts that are able to serve your application using the ALLOWED_HOSTS setting.
# This is a security measure to prevent HTTP host header attacks.

# Application definition

INSTALLED_APPS = [
    'account.apps.AccountConfig',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'django_extensions',
    'images.apps.ImagesConfig',
    'easy_thumbnails',
    'actions.apps.ActionsConfig',
]

# In order to test the social authentication functionality serving your site through HTTPS,
# you are going to use the RunServerPlus extension of the package Django Extensions.
# Django Extensions is a third-party collection of custom extensions for Django.

MIDDLEWARE = [
    # Middleware are classes with methods that are globally executed during the request or response phase.
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bookmarks.urls'

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

WSGI_APPLICATION = 'bookmarks.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
# STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "account/static/"),
    )

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'dashboard'
# Tells Django which URL to redirect the user to after a successful login if no next parameter is present in the request.
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
# You are using the names of the URL patterns that you previously defined using the name attribute of the path() function.

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# To enable Django to serve media files uploaded by users with the development server
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
# MEDIA_URL is the base URL used to serve the media files uploaded by users, and
# MEDIA_ROOT is the local path where they reside. You build the path dynamically
# relative to your project path to make your code more generic.


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'account.authentication.EmailAuthBackend',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.google.GoogleOAuth2',
]

SOCIAL_AUTH_FACEBOOK_KEY = '606087041711702'  # Facebook ID
SOCIAL_AUTH_FACEBOOK_SECRET_KEY = 'e128912aa8ce6cefdb269b9ec53077a7'  # Facebook Secret Key
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

SOCIAL_AUTH_TWITTER_KEY = 'o9b76rNaYA290mRdEUEOdWBka'  # Twitter API Key
SOCIAL_AUTH_TWITTER_SECRET = 'uYcg20jst8prDrl1NC8cmjvBqxhg5wwjiV2LT5CzdGts9piTYJ'  # Twitter API Secret
# TWITTER_CLIENT_ID = 'Mi1lWEFuSVh4THJrajhPUGJnUk46MTpjaQ'
# TWITTER_CLIENT_SECRET_KEY = 'OU7cbNmTwWR8FoDWr5YqXzByYJ0zDeZS10hfzpxdmCB3ef5Xkb'

SOCIAL_AUTH_GOOGLE_OAUTH2_CLIENT_ID = '581823848282-llqe7nnat00hd8u2tp9hd5ruv6gpbae1.apps.googleusercontent.com'  # Google Consumer key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'  # Google API Consumer Secret


#  Another way to specify the URL for a model is by adding the ABSOLUTE_URL_OVERRIDES setting
ABSOLUTE_OVERRIDES = {
    'auth.user': lambda u: reverse_lazy('user_detail', args=[u.username])
}

THUMBNAIL_DEBUG = True

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

