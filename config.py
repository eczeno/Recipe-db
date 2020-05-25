from os import getenv, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

SQLALCHEMY_TRACK_MODIFICATIONS = False
TESTING = False
DEBUG = False
FLASK_ENV = 'development'
SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL')
SECRET_KEY = getenv('SECRET_KEY')