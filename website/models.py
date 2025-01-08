from . import db    #importing db object from __init__.py
from flask_login import UserMixin # type: ignore
#UserMixin help with user authentication and session management
from sqlalchemy.sql import func

class Note(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    data=db.Column(db.String(10000))
    date=db.Column(db.DateTime(timezone=True), default=func.now())  #automatically add DATE
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))         #One user Multiple Notes
    
class User(db.Model, UserMixin):  #user table
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(120), nullable=False, unique=True)
    password=db.Column(db.String(120), nullable=False)
    first_name=db.column(db.String(120))
    notes=db.relationship('Note')        #all users to be able to find all of their Note
