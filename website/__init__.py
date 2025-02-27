from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db=SQLAlchemy()
DB_NAME='database.sqllite3'  #db name

#fun to create db
def create_database():
    db.create_all()
    print('OK created')


def create_app():
    from flask import Flask

    app = Flask(__name__)

    app.config['SECRET_KEY']="parulhardaha"
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  #Added this line to ignore

    db.init_app(app)  #initialie db with app

    login_manager=LoginManager() #keep track of customer,who have logged in
    login_manager.init_app(app)
    login_manager.login_view='auth.login'

    #identify user acc to thier primary key
    @login_manager.user_loader
    def load_user(id):
        return Customer.query.get(int(id))

    from .views import views
    from .admin import admin
    from .auth import auth
    from .models import Customer, Cart, Product, Order

    #register these blp using app variable
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    #calling create_dp function
    with app.app_context():
        create_database()
    
    return app