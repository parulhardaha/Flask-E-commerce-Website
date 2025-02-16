from . import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash # comes with flask login

class Customer(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    email=db.Colmun(db.String(50), unique=True)
    username=db.Colmun(db.String(100))
    password_hash=db.Colmun(db.String(50))
    date_joined=db.Column(db.DateTime(), default=datetime.utcnow)


    # for password hashing
    @property
    def password(self):
        raise AttributeError('Password is not a readable Attribute')

    @password.setter
    def password(self, password):
        self.password_hash=generate_password_hash(password=password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password=password)

    def __str__(self):
        return '<Customer %r>' % Customer.id  
        #print (Customer2)--> Customer 2

        
