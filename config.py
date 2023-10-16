import os
from datetime import timedelta

# Base directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config():
    # Debug mode
    FLASK_DEBUG = True
    FLASK_ENV = 'development'
    TEMPLATES_AUTO_RELOAD = True

    # CSRF
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = 'secret'

    # Session
    SECRET_KEY = '638fac048ac09b5dd8f596aa0a479a94'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)
    
    # SQL Alchemy Database settings
    USERNAME = 'postgres'
    PASSWORD = 'phong1202'
    DATABASE_NAME = 'todolist_db'
    SQLALCHEMY_DATABASE_URI = f'postgresql://{USERNAME}:{PASSWORD}@localhost/{DATABASE_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False