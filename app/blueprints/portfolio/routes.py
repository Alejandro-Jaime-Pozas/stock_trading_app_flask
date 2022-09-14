from crypt import methods
from . import bp as portfolio
from flask import jsonify, request
from ..auth.http_auth import token_auth
# from .models import Stock # when models is complete remove comment

# on the app, will need routes to: 
# create a new stock (buy a new stock you don't own)        POST, token auth
@portfolio.route('/stocks', methods=["GET", "POST" ])
@token_auth.login_required
def create_stock():
    # need to receive user info on stock, including price, shares, and remove the total $ amount from cash portfolio, add to stock
    pass


# get all user's stocks (show user a list of his stocks)    GET, token auth
@portfolio.route('/<int:id>', methods=["GET", ])
@token_auth.login_required
def get_stocks():
    # need to get the user's id, and then get all of that user's stocks from stock table with that user id
    pass


# update a stock (add/remove funds)                         PUT, token auth
@portfolio.route('/stocks/<int:stock_id>', methods=["GET", "PUT"])
@token_auth.login_required
def update_stock():
    # can only update the share amount of stock, not price. take the shares to sell/buy and add/remove from stock shares amount
    pass


# delete a stock (if remove all funds from stock)           DELETE, token auth
@portfolio.route('/stocks/<int:stock_id>', methods=["GET", "DELETE"])
@token_auth.login_required
def delete_stock():
    # only do this if user removes all shares, so shares equals 0 after the user sells all of his shares (maybe need to add btn to react frontend to remove/delete all shares...)
    pass