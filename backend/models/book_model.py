from global_vars.database_init import db
from flask_login import UserMixin
from sqlalchemy import CheckConstraint
from dataclasses import dataclass

@dataclass
class Book(db.Model):
    __tablename__ = 'book'
    id:int = db.Column(db.Integer, primary_key=True)
    stock:int = db.Column(db.Integer)
    title:str = db.Column(db.String(300))
    publish_year:int = db.Column(db.Integer)
    description:str = db.Column(db.String(1000))
    isbn:str = db.Column(db.String(100))

@dataclass
class BookLanguage(db.Model):
    __tablename__ = 'booklanguage'
    id:int = db.Column(db.Integer, primary_key=True)
    bookId:int = db.Column(db.Integer, db.ForeignKey('book.id'))
    language:str = db.Column(db.String(50))

@dataclass
class Genre(db.Model):
    __tablename__ = 'genre'
    id:int = db.Column(db.Integer, primary_key=True)
    name:str = db.Column(db.String(100))

@dataclass
class BookGenre(db.Model):
    __tablename__ = 'bookgenre'
    id:int = db.Column(db.Integer, primary_key=True)
    bookId:int = db.Column(db.Integer, db.ForeignKey('book.id'))
    genreId:int = db.Column(db.Integer, db.ForeignKey('genre.id'))

@dataclass
class Author(db.Model):
    __tablename__ = 'author'
    id:int = db.Column(db.Integer, primary_key=True)
    name:str = db.Column(db.String(150))
    place:str = db.Column(db.String(300))

@dataclass
class BookAuthor(db.Model):
    __tablename__ = 'bookauthor'
    id:int = db.Column(db.Integer, primary_key=True)
    bookId:int = db.Column(db.Integer, db.ForeignKey('book.id'))
    authorId:int = db.Column(db.Integer, db.ForeignKey('author.id'))

@dataclass
class BookImage(db.Model):
    __tablename__ = 'bookimage'
    id:int = db.Column(db.Integer, primary_key=True)
    bookId:int = db.Column(db.Integer, db.ForeignKey('book.id'))
    image:str = db.Column(db.String(500))

@dataclass
class BookFile(db.Model):
    __tablename__ = 'bookfile'
    id:int = db.Column(db.Integer, primary_key=True)
    bookId:int = db.Column(db.Integer, db.ForeignKey('book.id'))
    fileSrc:str = db.Column(db.String(500))

@dataclass
class BookLocation(db.Model):
    __tablename__ = 'booklocation'
    id: int = db.Column(db.Integer, primary_key=True)
    bookId:int = db.Column(db.Integer, db.ForeignKey('book.id'))
    roomId: str = db.Column(db.String(30))
    shelfId: str = db.Column(db.String(30))
