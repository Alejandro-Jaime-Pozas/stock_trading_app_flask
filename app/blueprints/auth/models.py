from app import db
import os
import base64
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

# create user class that has username, email, password, password hash, create date 
class User(db.Model): # this calls Model class from SQLAlchemy db instance
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    pwd_hash = db.Column(db.String(128), nullable=False) 
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    token = db.Column(db.String(64), unique=True, index=True) # COME BACK index
    token_expiration = db.Column(db.DateTime)
    cash = db.Column(db.Integer, default=0)
    stocks = db.relationship('Stock', backref='owner', lazy=True) # COME BACK lazy

    # need fns to CRUD user
    def __init__(self, **kwargs):
        super().__init__(**kwargs) # super() passing in new kwargs to existing db.Model attributes
        self.pwd_hash = generate_password_hash(kwargs['password']) # kwargs here is a dict from def __init__ of User; changing the state of password to a hashed version
        # print(type(kwargs))
        db.session.add(self)
        db.session.commit()
        # could add cash acct here..but should it be a part of the user table better? YES bc table updates

    def __repr__(self):
        return f"<User|{self.username}, {self.email}>"

    def cash_balance(self):
        # the user will either press deposit/add or withdraw funds button on react..create handleClick for each 
        # both add/remove funds are put methods, changing the value of the cash attr...need token and body
        pass

    def check_password(self, password):
        return check_password_hash(self.pwd_hash, password)

    def get_token(self, expires_in=3600): # COME BACK
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(minutes=1): # this checks to see if there is an existing token for user
            return self.token
        self.token = base64.b64encode(os.urandom(16)).decode('utf-8') # this is gibberish
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.commit() # why no db.session.add?? bc there already exists a user instance
        return self.token

    def delete(self):
        db.session.delete(self) # it seems like delete is a fn from the db.session module...
        db.session.commit()

    def update(self, data): # COME BACK
        for field in data:
            if field not in {'username', 'email', 'password', 'cash'}: 
                continue
            # if not data[field]:
            #     continue
            if field == 'password':
                setattr(self, field, generate_password_hash(data[field])) # for dictionaries, sets self (user instance)'s pwd to new hash pwd to be able to compare encrypted pwd to real pwd
            if field == 'cash':
                setattr(self, field, self.cash + int(data[field]))
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
            'cash': self.cash
        }
