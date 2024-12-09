from pathlib import Path
from decouple import config
from .settings import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG_PROD', cast=bool)

CSRF_TRUSTED_ORIGINS = [
    'https://rmcoder.org',
    'https://www.rmcoder.org',
]
ALLOWED_HOSTS = [
    'rmcode.org',
    'www.rmcode.org',
    '201.6.156.10',
]

INSTALLED_APPS = [
    'tailwind',
    'theme',
]

MIDDLEWARE = []

# SESSION_COOKIE_AGE = 1209600  # 2 weeks, in seconds

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime}  {process:d}  {message}',
            'style': '{',
        },
    },
    'handlers': {
        'newfile': {
            ''
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/home/rm/www/rmcode/logs/djangoLog.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['newfile'],
            'propagate': False,
        },
    },
}
