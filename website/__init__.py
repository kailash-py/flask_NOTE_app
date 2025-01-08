from flask import Flask # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from os import path
from flask_login import LoginManager
db=SQLAlchemy() #DB object
DB_NAME='database.db'


def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='qwert asdfg'             #Encrypt the cookies and session data
    app.config['SQLALCHEMY_DATABASE_URI']= f'sqlite:///{DB_NAME}'
    db.init_app(app)



    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note #importing models.py
    with app.app_context():
        create_database(app)
    login_manager=LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):          #load the user
        return User.query.get(int(id))


    return app

def create_database(app):
    if not path.exists('website/'+ DB_NAME):
        db.create_all()      #we need to pass 'app' because tell flask sqlalchemy which app we are creating the database for
        print('Databse Created')

    