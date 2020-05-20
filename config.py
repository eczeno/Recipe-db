from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

TESTING = False
DEBUG = False
FLASK_ENV = 'development'
SQLALCHEMY_DATABASE_URI = 'sqlite:///recipe.db'
SECRET_KEY = environ.get('SECRET_KEY')