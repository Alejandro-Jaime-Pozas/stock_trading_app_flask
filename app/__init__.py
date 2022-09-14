# create the flask app here and all its main fns/references...
from flask import Flask # Flask class from the flask package
from config import Config # this config refers to class in file config.py, refers to database stuff
from flask_sqlalchemy import SQLAlchemy # SQLAlchemy package allows python > sql tables/translation/communication?
from flask_migrate import Migrate # migrate allows for new data to populate in database?
from flask_cors import CORS


app = Flask(__name__) # calls Flask class in flask package with input __name__
app.config.from_object(Config)
# app.config['SECRET_KEY'] = 'you-will-never-guess' # creates a secret key into app into config which is
# the subclass of a dict and acts the same as a dict
# this secret key is a CSRF token that needs to be validated before being submitted

# add flask-cors cross-origin resource sharing
CORS(app)

# create an instance of SQLAlchemy (the ORM) w the Flask Application
db = SQLAlchemy(app)
# create an instance of Migrate which will be our migration engine and pass in the app and SQLAlchemy instance
migrate = Migrate(app, db)

### import blueprints into the app flask instance for auth and portfolio
from app.blueprints.auth import bp as auth
app.register_blueprint(auth)
from app.blueprints.portfolio import bp as portfolio
app.register_blueprint(portfolio)

from app import routes # you need to include this AFTER flask instance to avoid infinite loop...the . refers to the current folder; 