from app import db
from datetime import datetime
from app.blueprints.auth.models import User
from flask import jsonify

class Stock(db.Model): # would want to add transaction history...so instead of just Stock model, buy/sell model too
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(8), nullable=False) # not unique since multiple users can have same stock
    new_price = db.Column(db.Float, nullable=False)
    new_shares = db.Column(db.Integer, nullable=False)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # why no () for utcnow? for some reason should store the function itself, not function call
    total_shares = db.Column(db.Integer) # no user input req, these are all calculated with methods in flask
    total_invested = db.Column(db.Float) # no user input req, these are all calculated with methods in flask
    total_divested = db.Column(db.Float) # no user input req, these are all calculated with methods in flask
    avg_price = db.Column(db.Float) # no user input req, these are all calculated with methods in flask
    real_value = db.Column(db.Float) # no user input req, these are all calculated with methods in flask
    transactions = db.relationship('Transaction', backref='the_stock', lazy=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # 'user.id' refers to User class, their id primary key...; this accepts an input either as string or integer and turns to integer


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'< Stock {self.ticker}|user id {self.user_id}'

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
        if not self.total_shares:
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
            'owner': User.query.get(self.user_id).to_dict() # this returns the User to_dict() fn from User class...smart
        }
    

# this transaction could either be buy/sell of user stocks, or add/remove funds. and in future should support other transactions such as savings acct, bank transfers etc.
class Transaction(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    transaction_type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float)
    cash_in = db.Column(db.Boolean, nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stock = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit() # no need to include obj in commit()