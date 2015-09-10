"""
Django settings for trydjango18 project.

Generated by 'django-admin startproject' using Django 1.8.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'm09p(gd68lzjo5=z-y-isrmb1)#onhsxz3wpw4za4@#&rnl)(j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

#For Email
#***********
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'bioinformaticsproject42@gmail.com'   #From Email:see Views Contact   #need to unlock Captcha under accounts.google.com/displayunlockcaptcha
EMAIL_HOST_PASSWORD = 'Slulo1970'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
#ACCOUNT_EMAIL_VERIFICATION = 'none'
#***********


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'django.contrib.sites',     #for registr
    #third party
    'crispy_forms',
    'jquery',
    #'registration',  #just used with models.py SignUp..
    #my apps
    'UserAccounts',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'trydjango18.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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


WSGI_APPLICATION = 'trydjango18.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'   #serve static files
STATIC_ROOT = os.path.join(BASE_DIR, "static_in_pro", "static_root")  #server where  it --goes to--
#STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_in_env", "static_root")


STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static_in_pro", "our_static"),  #where we keep -our- statics

)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "static_in_pro", "media_root")
#MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_in_env", "media_root")

#Crispy
CRISPY_TEMPLATE_PACK = 'bootstrap3'

#Registration
ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window
REGISTRATION_AUTO_LOGIN = True # Automatically log the user at signup


#login
SITE_ID = 4   #why 4?  See below:
#>>> from django.contrib.sites.models import Site
#>>> site = Site.objects.create(domain='example.com', name='example.com')
#>>> site.save()
#then lookup the Site-Id:
#>>>Site.object.all()[0].pk
#Logins go to main page! not landing!
LOGIN_REDIRECT_URL = 'main'