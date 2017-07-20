import os
import sys
import configparser

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = configparser.ConfigParser(allow_no_value=True)
config.read(os.getenv('CONFIG_FILE', BASE_DIR + '/docker/config.ini'))

db_password = os.getenv('DB_PASSWORD', config['database']['password'])
if os.path.isfile(db_password):
    with open(db_password, 'r') as password_file:
        db_password = password_file.read()

DEBUG = os.getenv('DEBUG', config['site']['debug']).lower() == 'true'

SITE_ROOT = os.getenv('SITE_URL', config['site']['url'])
SITE_NAME = os.getenv('SITE_NAME', config['site']['name'])
PING_ENDPOINT = SITE_ROOT + "/ping/"
DEFAULT_FROM_EMAIL = os.getenv('MAIL_FROM', config['mail']['default_from'])

DATABASES = {
   'default': {
       'ENGINE': os.getenv('DB_ENGINE', config['database']['engine']),
       'NAME': os.getenv('DB_NAME', config['database']['name']),
       'USER': os.getenv('DB_USER', config['database']['user']),
       'PASSWORD': db_password,
       'HOST': os.getenv('DB_HOST', config['database']['host']),
       'TEST': {'CHARSET': 'UTF8'}
   }
}

# Email
EMAIL_HOST = os.getenv('MAIL_HOST', config['mail']['host'])
EMAIL_PORT = os.getenv('MAIL_PORT', config['mail']['port'])
EMAIL_HOST_USER = os.getenv('MAIL_USER', config['mail']['user'])
EMAIL_HOST_PASSWORD = os.getenv('MAIL_PASSWORD', config['mail']['password'])
EMAIL_USE_TLS = os.getenv('MAIL_TLS', config['mail']['use_tls']).lower() == 'true'

REGISTRATION_OPEN = os.getenv('ENABLE_REGISTRATION', config['site']['enable_registration']).lower() == 'true'

ALLOWED_HOSTS = ['*']
COMPRESS_OFFLINE = True
MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'hc.accounts.middleware.TeamAccessMiddleware',
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
