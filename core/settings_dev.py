from pathlib import Path
from decouple import config
from .settings import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

CSRF_TRUSTED_ORIGINS = [
    'http://localhost',
]
ALLOWED_HOSTS = [
    'localhost', '192.168.0.50'
]

TAILWIND_APP_NAME = 'theme'

INTERNAL_IPS = [
    "127.0.0.1",
]

INSTALLED_APPS = [
    'tailwind',
    'theme',
]

MIDDLEWARE = []
