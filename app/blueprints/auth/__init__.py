from flask import Blueprint

# create instance of Blueprint with name, import name, and url value for online navigation/reference
bp = Blueprint('auth', __name__, url_prefix='/auth')

# import the routes for /auth to save them into the main app...
from . import routes, models