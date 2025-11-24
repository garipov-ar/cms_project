import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY=os.getenv('DJANGO_SECRET_KEY','123')
DEBUG=os.getenv('DJANGO_DEBUG','1')=='1'
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,web').split(',')
MEDIA_HOST = os.getenv('DJANGO_MEDIA_HOST', 'http://localhost:8000')



INSTALLED_APPS=[
 'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes',
 'django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles',
 'rest_framework','cms_app'
]

MIDDLEWARE=[
 'django.middleware.security.SecurityMiddleware',
 'django.contrib.sessions.middleware.SessionMiddleware',
 'django.middleware.common.CommonMiddleware',
 'django.middleware.csrf.CsrfViewMiddleware',
 'django.contrib.auth.middleware.AuthenticationMiddleware',
 'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF='project_settings.urls'
WSGI_APPLICATION='project_settings.wsgi.application'

DATABASES={'default':{
 'ENGINE':'django.db.backends.postgresql',
 'NAME':os.getenv('POSTGRES_DB'),
 'USER':os.getenv('POSTGRES_USER'),
 'PASSWORD':os.getenv('POSTGRES_PASSWORD'),
 'HOST':os.getenv('POSTGRES_HOST'),
 'PORT':os.getenv('POSTGRES_PORT'),
}}

STATIC_URL='/static/'
STATIC_ROOT=BASE_DIR/'staticfiles'
MEDIA_URL='/media/'
MEDIA_ROOT=BASE_DIR/'media'
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


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
