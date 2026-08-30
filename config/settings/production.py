import os
from .base import *




# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = []




STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# Database
DATABASES = {
 'default': {
   'ENGINE': 'django.db.backends.postgresql',
   'NAME': os.getenv('POSTGRES_DB'),
   'USER': os.getenv('POSTGRES_USER'),
   'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
   'HOST': os.getenv('POSTGRES_HOST'),
   'PORT': os.getenv('POSTGRES_DB_PORT', 5432),
   'OPTIONS': {
     'sslmode': 'require',
   },
 }
}
