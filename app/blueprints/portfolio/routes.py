from . import bp as portfolio
from flask import jsonify, request
from ..auth.http_auth import token_auth
from .models import Stock # when models is complete remove comment
from ..auth.models import User
from app import db

# need to acct for the change in cash balance for user after every transaction
# on the app, will need routes to: 

# create a new stock (buy a new stock you don't own)        POST, token auth
@portfolio.route('/stocks', methods=["GET", "POST" ])
@token_auth.login_required
def create_stock():
    if not request.is_json:
        return jsonify({'error': 'Please send a body'}), 400
    # receive user info on stock, including price, shares, remove the total $ amount from cash portfolio, add to stock portfolio
    # fetch req from frontend
    data = request.json
    # take data from body, create new Stock if body conditions met ;frontend check if stock is new, if not do PUT method instead
    cash_needed = 1
    for field in {'ticker', 'new_price', 'new_shares'}:
        if field not in data:
            return jsonify({'error': f'Need to include {field} in req body'}), 400 # bad req
        if field in {'new_price', 'new_shares'}:
            cash_needed *= data[field]
    current_user = token_auth.current_user()
    if cash_needed > current_user.cash: # IF USER INPUTS MORE SHARES THAN THEIR CASH ACCT BALANCE
        return jsonify({'error': f'Not enough funds for transfer'}), 400
    # dont think I need this for loop below bc react frontend covers it..
    for stock in current_user.stocks:
        if stock.ticker == data['ticker']:
            return jsonify({'error': f'You already have {stock.ticker} in your stocks.'}), 400 # bad req
    data['user_id'] = current_user.id # here we are adding a field to dictionary of data that would read {'user_id': 1}
    new_stock = Stock(**data)
    new_stock.calculations()
    current_user.cash -= new_stock.new_price * new_stock.new_shares 
    db.session.commit()
    return jsonify(new_stock.to_dict()), 201 # success

# get all the user's stocks (show user a list of his stocks)    GET, token auth
@portfolio.route('/<int:user_id>', methods=["GET", ])
@token_auth.login_required
def get_stocks(user_id):
    # need to get the user's id, and then get all of that user's stocks from stock table with that user id
    current_user = token_auth.current_user()
    if current_user.id != user_id:
        return jsonify({'error': f'Your user id of {current_user.id} is not authorized to get these stocks'}), 401
    return jsonify([stock.to_dict() for stock in current_user.stocks]), 201 # this is returning a list, need to make it json type...


# update a stock (add/remove funds)                         PUT, token auth
# NEED TO CHECK IF USER INPUTS MORE SHARES THAN THEY OWN FOR THAT STOCK..COMPARE THE STOCK BEFORE CHANGING ITS NEW_SHARES...
@portfolio.route('/stocks/<int:stock_id>', methods=["GET", "PUT"])
@token_auth.login_required
def update_stock(stock_id):
    # can only update the share amount of stock, price, not ticker. take the shares to sell/buy and add/remove from stock shares amount
    data = request.json
    cash_needed = 1
    stock = Stock.query.get_or_404(stock_id) # returns a not found msg to frontend if 404
    for field in {'new_price', 'new_shares'}:
        if field not in data:
            return jsonify({'error': f'The {field} field is required'}), 400
        elif field == 'new_shares':
            # check if user inputs more shares than they own
            if -data['new_shares'] > stock.total_shares: # check maybe int is needed..
                return jsonify({'error': f'You only have {stock.total_shares} shares to sell'}), 400  
            elif data['new_shares'] == 0:
                return jsonify({'error': f'You need to sell at least 1 share'}), 400  
        cash_needed *= data[field]
    current_user = token_auth.current_user()
    if current_user.id != stock.user_id:
        return jsonify({'error': f'You are not authorized to edit this stock id\'s values'}), 401
    user = User.query.get(stock.user_id)
    # check if user inputs more shares than they can afford
    if cash_needed > user.cash: # IF USER INPUTS MORE SHARES THAN THEIR CASH ACCT BALANCE
        return jsonify({'error': f'Not enough funds for transfer'}), 400
    stock.update(data) # NEED TO CHECK IF THE USER INPUTS ALL SHARES THEY OWN, MUST SELL ALL, AND DELETE STOCK
    # check if user bought or sold shares, to add to cash acct or remove from it
    if stock.new_shares > 0:
        user.cash -= stock.new_price * stock.new_shares
    else:
        user.cash += stock.new_price * -stock.new_shares
    # check if user sold all of the stock
    if stock.total_shares == 0:
        stock.delete()
    db.session.commit()
    return jsonify(stock.to_dict())


# delete a stock (if remove all funds from stock), dont think i'll need it....           DELETE, token auth
@portfolio.route('/stocks/<int:stock_id>', methods=["GET", "DELETE"])
@token_auth.login_required
def delete_stock(stock_id):
    # only do this if user removes all shares, so shares equals 0 after the user sells all of his shares (maybe need to add btn to react frontend to remove/delete all shares...)
    data = request.json
    for field in {'new_price', 'new_shares'}:
        if field not in data:
            return jsonify({'error': f'The {field} field is required'}), 400
    stock = Stock.query.get_or_404(stock_id)
    current_user = token_auth.current_user()
    if current_user.id != stock.user_id:
        return jsonify({'error': f'You are not authorized to delete this stock with stock id # {stock_id}'}), 401
    current_user.cash -= stock.new_price * stock.new_shares
    stock.delete(data)
    db.session.commit()
    return jsonify({'success': f'You have successfully deleted all of your {stock.total_shares} shares of {stock.ticker} stock'}), 201 # strange this still prints out stock even though it was just deleted one line earlier..maybe to do with it being in a fn?