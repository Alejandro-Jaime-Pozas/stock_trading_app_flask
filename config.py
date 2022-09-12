# setup db location on local/live server
import os

basedir = os.path.abspath(os.path.dirname(__file__)) # COME BACK

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess' # COME BACK
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db') # COME BACK
    SQLALCHEMY_TRACK_MODIFICATIONS = False # COME BACK