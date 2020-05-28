from os import getenv, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

SQLALCHEMY_TRACK_MODIFICATIONS = False
TESTING = False
FLASK_ENV = 'development'
# FLASK_ENV = 'production'
if FLASK_ENV == 'production':
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL')
    DEBUG = False
else:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///recipe.db'
    DEBUG = True

SECRET_KEY = getenv('SECRET_KEY')