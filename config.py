"""Flask configuration."""
from os import environ, path, getenv
import os
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

print('--------SECRET_KEY--------')
print(os.getenv('SECRET_KEY'))
print('--------SECRET_KEY--------')

class Config:
    """Base config."""
    # SECRET_KEY = os.getenv('SECRET_KEY') # In case the key is stored in our os for ex windows' system-env
    SECRET_KEY = environ.get('SECRET_KEY') # In our case the key is stored in our ./.env file 
    # SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')