from global_vars.database_init import db
from flask_login import UserMixin
from sqlalchemy import CheckConstraint
from models.book_model import Book
from dataclasses import dataclass

@dataclass
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id:int = db.Column(db.Integer, primary_key=True)
    email:str = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(530))
    name:str = db.Column(db.String(300))
    role:str = db.Column(db.String(20))
    isRestricted:bool = db.Column(db.Boolean, default=False)
    
@dataclass
class Comment(db.Model):
    __tablename__ = 'comment'
    #Note that SQLAlchemy will auto increment the ID if the there's a single integer primary key
    # and not a foreign key 
    id:int = db.Column(db.Integer, primary_key=True) 
    userId:int = db.Column(db.Integer, db.ForeignKey('user.id')) 
    comment:str = db.Column(db.String(3000))
    rating:int = db.Column(db.Integer)
    bookId:int = db.Column(db.Integer, db.ForeignKey('book.id'))

