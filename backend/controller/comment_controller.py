from models.user_model import User, Comment
from models.book_model import Book
from models.user_book import BookBorrow, BookFavorite
from sqlalchemy import select, func, distinct
from global_vars.database_init import db
import json
from global_vars.errors import *
from datetime import datetime, timedelta
from flask_login import login_user, login_required, current_user, logout_user
from global_vars.constants import *



def add_comment(userId: int, bookId: int, comment: str, rating: int):
    user = db.session.query(User).filter(User.id == userId).first()
    book = db.session.query(Book).filter(Book.id == bookId).first()
    if not user or not book:
        return False, None, ADD_ENTRY_ERROR
    else:
        new_comment = Comment()
        new_comment.bookId = bookId
        new_comment.userId = userId
        new_comment.comment = comment
        new_comment.rating = rating
        db.session.add(new_comment)
        try:
            db.session.commit()
            return True, new_comment, None
        except:
            return False, None, ADD_ENTRY_ERROR

def edit_comment(commentId: int, commentStr: str, rating: int):
    comment = db.session.query(Comment).filter(Comment.id == commentId).first()
    if comment != None:
        comment.comment = commentStr
        comment.rating = rating
        try:
            db.session.commit()
            return True, comment, None
        except:
            return False, None, EDIT_ERROR
    else:
        return False, None, ROW_NOT_EXISTS

def delete_comment(commentId: int):
    deleted_rows = db.session.query(Comment).filter(Comment.id == commentId).delete()
    db.session.commit()
    return True, deleted_rows, None

def get_user_comment(userId: int, start_from: int=None, limit: int=None):
    user = db.session.query(User).filter(User.id == userId).first()
    if not user:
        return False, None, USER_NOT_EXIST
    else:
        query = select(Comment)
        query = query.filter(Comment.userId == userId)
        if start_from != None:
            query = query.offset(start_from)
        if limit != None:
            query = query.limit(limit)
        result = db.session.execute(query).all()
        result = [val[0] for val in result]
        return True, result, None

def get_book_comment(bookId: int, start_from: int=None, limit: int=None):
    book = db.session.query(Book).filter(Book.id == bookId).first()
    if not book:
        return False, None, INVALID_ID
    else:
        query = select(Comment)
        query = query.filter(Comment.bookId == book.id)
        if start_from != None:
            query = query.offset(start_from)
        if limit != None:
            query = query.limit(limit)
        result = db.session.execute(query).all()
        result = [val[0] for val in result]
        return True, result, None
    
def get_book_avg_rating(bookId: int):
    try:
        rating_sum, rating_count = db.session.query(func.sum(Comment.rating), func.count(distinct(Comment.bookId))).filter(Comment.bookId == bookId).first()
        average_rating = rating_sum / rating_count
        return True, average_rating, None
    except:
        return False, None, DATABASE_ERROR
    
