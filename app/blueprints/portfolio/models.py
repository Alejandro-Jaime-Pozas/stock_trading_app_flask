from app import db
from datetime import datetime
from app.blueprints.auth.models import User
# from flask import jsonify

class Stock(db.Model): # would want to add transaction history...so instead of just Stock model, buy/sell model too
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(8), nullable=False) # not unique since multiple users can have same stock
    new_price = db.Column(db.Float, nullable=False)
    new_shares = db.Column(db.Integer, nullable=False)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # why no () for utcnow? for some reason should store the function itself, not function call
    active = db.Column(db.Boolean, nullable=False, default=True) # if 0 shares, change to False
    total_shares = db.Column(db.Integer) # no user input req, these are all calculated with methods in flask
    total_invested = db.Column(db.Float) # no user input req, these are all calculated with methods in flask
    total_divested = db.Column(db.Float) # no user input req, these are all calculated with methods in flask
    avg_price = db.Column(db.Float) # no user input req, these are all calculated with methods in flask
    real_value = db.Column(db.Float) # no user input req, these are all calculated with methods in flask
    transactions = db.relationship('Transaction', backref='the_stock', lazy=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # 'user.id' refers to User class, their id primary key...; this accepts an input either as string or integer and turns to integer


    def __init__(self, **kwargs):
        super().__init__(**kwargs) # new_shares and new_price from Transaction should be included here
        self.update(kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<id: {self.id} | Stock {self.ticker}>'

    def update(self, data): # data is the dict of new_price and new_shares...
        # need to take the data in, change new_price and new_shares, and set new values for calculations...
        for key in data:
            setattr(self, key, data[key])
        self.calculations()
        db.session.commit()

    def calculations(self):
        # if self.new_price * self.new_shares > User.query.get(self.user_id).cash:
        #     return jsonify({'error': f'You do not have enough cash for this trade'}), 400
        # if for 1st instance when stock created
        if not self.total_shares: # WILL NEED TO ACCT FOR WHEN SHARES GO DOWN TO 0 IF USER SELLS ALL
            self.total_shares = self.new_shares
            self.total_invested = self.new_shares * self.new_price
            self.avg_price = self.new_price
            self.real_value = self.new_shares * self.new_price
            self.total_divested = 0
            db.session.commit()
        elif self.total_shares:
            self.total_shares += self.new_shares
            if self.new_shares > 0:
                self.total_invested += self.new_shares * self.new_price # this is sumproduct of past 
            if self.total_shares != 0:
                self.avg_price = self.total_invested / self.total_shares # this could be wrong since it depends on new total_invested
            self.real_value = self.total_shares * self.new_price # same here couold be wrong
            if self.new_shares < 0:
                self.total_divested += self.new_shares * self.new_price
            db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'ticker': self.ticker,
            'new_price': self.new_price,
            'new_shares': self.new_shares,
            'create_date': self.create_date,
            'total_shares': self.total_shares,
            'total_invested': self.total_invested,
            'total_divested': self.total_divested,
            'avg_price': self.avg_price,
            'real_value': self.real_value,
            'user_id': self.transactions[0].user_id if self.transactions else None # this returns the User to_dict() fn from User class...smart
        }
    

# this transaction could either be buy/sell of user stocks, or add/remove funds. and in future should support other transactions such as savings acct, bank transfers etc.
class Transaction(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # created
    transaction_type = db.Column(db.String(50), nullable=False) # stock vs cash
    amount = db.Column(db.Float) # cash only field
    ticker = db.Column(db.String(8)) # stock only field
    new_price = db.Column(db.Float) # stock only field
    new_shares = db.Column(db.Integer) # stock only field
    cash_in = db.Column(db.Boolean, nullable=False) # True or False
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # one user
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=True) # 0 or 1 stock

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # some logic here to update either the user's cash or the stock's data
        if self.transaction_type == 'cash':
            self.update_user_cash()
        elif self.transaction_type == 'stock':
            self.update_stock(**kwargs)
        db.session.add(self)
        db.session.commit() # no need to include obj in commit()

    def __repr__(self):
        return f"<Transaction | id={self.id} | type={self.transaction_type} | user_id={self.user_id} | ticker={self.ticker}"
    
    # if user transaction is deposit or withdrawal of cash, update the user's cash with new amount
    def update_user_cash(self):
        user = User.query.get(self.user_id) # this should work since user_id is in api endpoint, may need to alter to pass in from app url endpoint
        user.update({'cash': self.amount})
        return user.cash

    # if user transaction is buying/selling a stock, update stock if existing, or create new stock if not
    def update_stock(self, **kwargs):
        stock_exists = Transaction.query.filter(Transaction.ticker==self.ticker).first() # CHANGE THIS TO USER QUERY OF HIS TRANSACTIONS, AND CHECK IF TICKER WITHIN TRANSACTION HISTORY.
        # if user already owns the stock, then get the existing stock and update it with data
        if stock_exists:
            # if shares of this stock are 0 (stock deactivated) reactivate the stock
            if not stock_exists.active:
                stock_exists.active = True 
            stock_exists.update(
                ticker=self.ticker, 
                new_price=self.new_price, 
                new_shares=self.new_shares,
            ) # CHECK IF WORKS
        # if user doesn't own the stock, create new stock with data
        else:
            new_stock = Stock(
                ticker=self.ticker,
                new_price=self.new_price,
                new_shares=self.new_shares,
            ) # does this auto-link the stock to this transaction?
            self.stock_id = new_stock.id # IMPORTANT to specify relationship here

    def to_dict(self, ):
        return {
            'id': self.id,
            'datetime': self.datetime, 
            'transaction_type': self.transaction_type, 
            'amount': self.amount, 
            'ticker': self.ticker, 
            'new_price': self.new_price, 
            'new_shares': self.new_shares, 
            'cash_in': self.cash_in, 
            'user': User.query.get(self.user_id).to_dict(),
            'stock': Stock.query.get(self.stock_id).to_dict() if self.stock_id else None, # transaction could have a stock or not
        }