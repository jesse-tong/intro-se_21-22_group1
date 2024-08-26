from global_vars.database_init import db
from flask_login import UserMixin
from sqlalchemy import CheckConstraint, text
from models.user_model import User
from models.book_model import Book
from dataclasses import dataclass
from datetime import datetime

#Models to indicate the books which user has marked as favorite or borrowed
@dataclass
class BookBorrow(db.Model):
    __tablename__ = 'bookborrow'
    id:int = db.Column(db.Integer, primary_key=True)
    bookId:int = db.Column(db.Integer, db.ForeignKey('book.id'))
    userId:int = db.Column(db.Integer, db.ForeignKey('user.id'))
    startBorrow:datetime = db.Column(db.DateTime)
    endBorrow:datetime = db.Column(db.DateTime)
    hasReturned:bool = db.Column(db.Boolean)
    returnDate:datetime = db.Column(db.DateTime)
    isDamagedOrLost: bool = db.Column(db.Boolean, default=False)
    isApproved: bool = db.Column(db.Boolean, default=False)
    hasResolved: bool = db.Column(db.Boolean, default=False)
    renewPending: bool = db.Column(db.Boolean, default=False, server_default=text('0'))

@dataclass
class BookFavorite(db.Model):
    __tablename__ = 'bookfavorite'
    id:int = db.Column(db.Integer, primary_key=True)
    bookId:int = db.Column(db.Integer, db.ForeignKey('book.id'))
    userId:int = db.Column(db.Integer, db.ForeignKey('user.id'))


