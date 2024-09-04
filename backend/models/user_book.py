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

@dataclass
class LibraryPlace(db.Model):
    __tablename__ = 'library_place'
    id:int = db.Column(db.Integer, primary_key=True)
    haveComputer: bool = db.Column(db.Boolean, default=True)
    room: str = db.Column(db.String(50))

    @property
    def isInHoldOrUse(self):
        session = db.session.query(LibrarySession).filter(LibrarySession.placeId == self.id).first()
        if session:
            return True
        else:
            return False
    
    @property
    def isInUse(self):
        session = db.session.query(LibrarySession).filter(LibrarySession.placeId == self.id).filter(LibrarySession.inUse == True).first()
        if session:
            return True
        return False
        
    def addSession(self, userId, inUse: bool = True, startDate: datetime = None):
        new_session = LibrarySession(userId=userId, placeId=self.id, inUse=inUse, startDate=startDate)
        db.session.add(new_session)
        db.session.commit()

    def getSessions(self):
        sessions = db.session.query(LibrarySession).filter(LibrarySession.placeId == self.id).all()
        return sessions

#Represent in hold/in use library facility session
@dataclass
class LibrarySession(db.Model):
    __tablename__ = 'library_session'
    id:int = db.Column(db.Integer, primary_key=True)
    placeId: int = db.Column(db.Integer, db.ForeignKey('library_place.id'))
    userId: int = db.Column(db.Integer, db.ForeignKey('user.id'))
    inUse: bool = db.Column(db.Boolean, default=False)
    startDate: datetime = db.Column(db.DateTime)
    books = db.relationship('LibrarySessionBook', backref='library_session')
    def addBook(self, bookId:int):
        new_book = LibrarySessionBook(sessionId=self.id, bookId=bookId)
        db.session.add(new_book)
        db.session.commit()

    def editBook(self, bookId:int, newBookId:int):
        book = LibrarySessionBook.query.filter_by(sessionId=self.id, bookId=bookId).first()
        if book:
            book.bookId = newBookId
            db.session.commit()

    def deleteBook(self, bookId:int):
        book = LibrarySessionBook.query.filter_by(sessionId=self.id, bookId=bookId).first()
        if book:
            db.session.delete(book)
            db.session.commit()
    
    def getBorrowedBooks(self):
        books = db.session.query(Book).join(LibrarySessionBook, Book.id == LibrarySessionBook.bookId).filter(LibrarySessionBook.sessionId == self.id).all()
        return books
@dataclass
class LibrarySessionBook(db.Model):
    id:int = db.Column(db.Integer, primary_key=True)
    sessionId: int = db.Column(db.Integer, db.ForeignKey('library_session.id'))
    bookId: int = db.Column(db.Integer, db.ForeignKey('book.id'))


