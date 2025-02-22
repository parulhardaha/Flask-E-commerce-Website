from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .views import views
from .admin import admin
from .auth import auth

db=SQLAlchemy()
DB_NAME='database.sqllite3'  #db name

#fun to create db
def create_database():
    db.create_all()
    print('OK created')


def create_app():
    app= Flask(__name__)
    app.config['SECRET_KEY']="parulhardaha"
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'

    db.init_app(app)  #initialie db with app

    #register these blp using app variable
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    #calling create_dp function
    with app.app_context():
        create_database()
    
    return app