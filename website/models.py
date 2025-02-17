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

    cart_items=db.relationship('Cart', backref=db.backref('customer', lazy=True))
    orders=db.relationship('Order', backref=db.backref('customer', lazy=True))
    
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

class Product (db.Model):
    id= db.Column(db.Integer, primary_key=True)
    product_name=db.Column(db.String(100), nullable=False)
    current_name=db.Column(db.Float(100), nullable=False)    
    product_name=db.Column(db.String(100), nullable=False)    
    current_price=db.Column(db.Float(100), nullable=False)
    previous_price=db.Column(db.Float(100), nullable=False)
    in_stock=db.Column(db.Integer, nullable=False)
    product_picture=db.Column(db.String(100), nullable=False)
    flash_sale=db.Column(db.Boolean, nullable=False)
    date_added=db.Column(db.Datetime, default=datetime.utcnow)

    carts=db.relationship('Cart', backref=db.backref('product',lazy=True))
    orders=db.relationship('Order', bakref=db.backref('product', lazy=True))
    def __str__(self):
        return '<Product %r>' %self.product_name
    
class Cart(db.Model):  
    id=db.Column(db.Integer, primary_key=True)
    quantity=db.Column(db.Interger, nullable=False)

    customer_link=db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_link=db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    #cart_item_1.product.any col name of product table
    
    def __str__(self):
        return '<Cart %r>' %self.id

class Order(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    quantity=db.Column(db.Integer, nullable=False)
    price=db.Column(db.Float, nullable=False)
    status=db.Column(db.String(100), nullable=False)
    payment_id=db.Column(db.String(100), nullable=False)

    customer_link=db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_link=db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __str__(self):
        return '<Order %r>' %self.id 
      
