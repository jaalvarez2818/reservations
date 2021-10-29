import os
from dotenv import dotenv_values
from pathlib import Path

environ = dotenv_values()

BASE_DIR = Path(__file__).resolve().parent.parent

"""   
    PRODUCTION = 1 -->  Cargar las variables desde las variables entorno del sistema
    PRODUCTION = 0 -->  Cargar las variables desde el archivo .env
    
"""

PRODUCTION = bool(int(environ.get('PRODUCTION', os.environ.get('PRODUCTION'))))

if PRODUCTION:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = int(os.environ.get('DEBUG'))
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(',')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, os.environ.get('DATABASE_NAME')),
        }
    }

else:
    SECRET_KEY = environ.get('SECRET_KEY')
    DEBUG = not PRODUCTION
    ALLOWED_HOSTS = environ.get('ALLOWED_HOSTS').split(',')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, environ.get('DATABASE_NAME')),
        }
    }
