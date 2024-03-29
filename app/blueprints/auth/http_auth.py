from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from .models import User
from datetime import datetime


#instance of http basic authentication
basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password): # in other words, if user is not None and password is true
        return user

@token_auth.verify_token
def verify(token):
    user = User.query.filter_by(token=token).first()
    now = datetime.utcnow()
    if user and user.token_expiration > now:
        return user