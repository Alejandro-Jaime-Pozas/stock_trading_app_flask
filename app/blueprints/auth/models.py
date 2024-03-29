from app import db
import os, base64
from datetime import datetime, timedelta
# from app.blueprints.portfolio.models import Transaction
from werkzeug.security import generate_password_hash, check_password_hash

# create user class that has username, email, password, password hash, create date 
class User(db.Model): # this calls Model class from SQLAlchemy db instance
    """User class needs unique username and email, and standard password"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False) 
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    token = db.Column(db.String(64), unique=True, index=True) # COME BACK index
    token_expiration = db.Column(db.DateTime)
    cash = db.Column(db.Integer, default=0)
    transactions = db.relationship('Transaction', backref='the_user', lazy=True)
    stocks = db.relationship('Stock', backref='the_user', lazy=True) # COME BACK lazy

    # need fns to CRUD user
    def __init__(self, **kwargs):
        super().__init__(**kwargs) # super() passing in new kwargs to existing db.Model AND class level attributes
        self.password = generate_password_hash(kwargs['password']) # kwargs here is a dict from def __init__ of User; changing the state of password to a hashed version
        # print(kwargs) # for some reason only user input kwargs are printed..
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<User|id:{self.id}|username:{self.username},email:{self.email}>"

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_token(self, expires_in=3600): # COME BACK
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(minutes=1): # this checks to see if there is an existing token for user
            return self.token
        self.token = base64.b64encode(os.urandom(16)).decode('utf-8') # this is gibberish
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.commit() # why no db.session.add?? bc there already exists a user instance
        return self.token

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, data): # COME BACK
        for field in data:
            if field not in {'username', 'email', 'password', 'cash'}: 
                continue
            if field == 'password':
                new_hash = generate_password_hash(data[field])
                setattr(self, field, new_hash) # for dictionaries, sets self (user instance)'s pwd to new hash pwd to be able to compare encrypted pwd to real pwd
                continue 
            elif field == 'cash':
            # REMOVING THIS BELOW BC THROWING A CIRC REF ERROR
            #     # setattr(self, field, self.cash + int(data[field])) # going to change this to create a Transaction
            #     Transaction(
            #         transaction_type='cash',
            #         amount=data[field],
            #         user_id=self.id
            #     )
                continue 
            else:
                setattr(self, field, data[field])
        db.session.commit() # commit changes, dont add

    # create a json type object
    def to_dict(self): 
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'date_created': self.date_created,
            'cash': self.cash,
            'total_transactions': len(self.transactions)
        }
