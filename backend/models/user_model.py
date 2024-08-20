import json
from global_vars.database_init import db
from flask_login import UserMixin
from sqlalchemy import CheckConstraint, event, Connection
from sqlalchemy.orm import mapper, Session
from models.book_model import Book
from dataclasses import dataclass
from datetime import datetime
from utils.ap_utils import uri

class URIs(object):
    def __init__(self, **kwargs):
        for attr, values in kwargs:
            setattr(self, attr, values)

#Note that if we don't declare the type of each attribute in a dataclass class, it will be ignore
#when being jsonified, also the password will be hashed before stored in the database
@dataclass
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id:int = db.Column(db.Integer, primary_key=True)
    email:str = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(530)) 
    name:str = db.Column(db.String(300))
    role:str = db.Column(db.String(20))
    isRestricted:bool = db.Column(db.Boolean, default=False)
    isVerified:bool = db.Column(db.Boolean, server_default="0", default=False)

    

@dataclass
class UserFollowing(db.Model):
    __tablename__ = 'user_following'
    id:int = db.Column(db.Integer, primary_key=True) 
    follower:int = db.Column(db.Integer, db.ForeignKey('user.id'))
    followedUser:int = db.column(db.Integer)
    #followedUser:int = db.column(db.Integer, db.ForeignKey('user.id'))

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


@dataclass
class CommentLike(db.Model):
    __tablename__ = 'comment_like'
    id:int = db.Column(db.Integer, primary_key=True)
    commentId:int = db.Column(db.Integer, db.ForeignKey('comment.id'))
    userId:int = db.Column(db.Integer, db.ForeignKey('user.id'))

@dataclass
class UserNotification(db.Model):
    id:int = db.Column(db.Integer, primary_key=True)
    userId:int = db.Column(db.Integer, db.ForeignKey('user.id'))
    notification:str = db.Column(db.String(3000))
    date:datetime = db.Column(db.DateTime)

@dataclass
class UserInfo(db.Model):
    id:int = db.Column(db.Integer, primary_key=True)
    userId:int = db.Column(db.Integer, db.ForeignKey('user.id'))
    age: int = db.Column(db.Integer)
    gender:str = db.Column(db.String(10))
    maxBorrow: int = db.Column(db.Integer)
    borrowLeft: int = db.Column(db.Integer)
    phone:str = db.Column(db.String(20))
    address: str = db.Column(db.String(500))
    imagePath: str = db.Column(db.String(300)) 

@dataclass
class Session(db.Model):
    __tablename__ = 'session'
    id:int = db.Column(db.Integer, primary_key=True)
    userId:int = db.Column(db.Integer, db.ForeignKey('user.id'))
    os:str = db.Column(db.String(50))
    browser:str = db.Column(db.String(50))
    referer:str = db.Column(db.String(500))
    ipAddress:str = db.Column(db.String(500))
    sessionTime: datetime = db.Column(db.DateTime, default=datetime.now)
