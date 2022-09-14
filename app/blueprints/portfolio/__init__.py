from flask import Blueprint

# create instance of Blueprint with name, import name, and url value for online navigation/reference
bp = Blueprint('portfolio', __name__, url_prefix='/portfolio')

# import the routes for /auth to save them into the main app...
from . import routes, models