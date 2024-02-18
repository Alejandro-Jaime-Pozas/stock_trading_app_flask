# setup db location on local/live server
import os

basedir = os.path.abspath(os.path.dirname(__file__)) # COME BACK
print(__file__)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess' # gets key from the running app environment and if None, returns sarcastic 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db') # if there is an env variable with key 'DATABASE_URL', set to that, if not sqlite
    SQLALCHEMY_TRACK_MODIFICATIONS = False # COME BACK