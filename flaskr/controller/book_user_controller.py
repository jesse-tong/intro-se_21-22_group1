from werkzeug.security import generate_password_hash, check_password_hash
from models.user_model import User
from models.book_model import Book, BookFile
from models.user_book import BookBorrow, BookFavorite
from sqlalchemy import select
from global_vars.database_init import db
from global_vars.errors import *
from datetime import datetime, timedelta
from dateutil.parser import parse as dateparse
from global_vars.constants import *
from global_vars.init_env import *
borrow_time = os.environ.get('DEFAULT_BORROW_TIMEOUT')
overdue_fine = os.environ.get('OVERDUE_FINE_PER_DAY')
overdue_limit_before_treated_as_lost = os.environ.get('OVERDUE_DAYS_LIMIT_BEFORE_LOST')
damage_and_lost_fine = os.environ.get('DAMAGE_AND_LOST_FINE')


#Default if start_date is null is the current date
def borrow_book(userId: int, bookId: int, start_date: datetime=None, end_date: datetime=None):
    borrow_book = BookBorrow()
    if start_date != None:
        borrow_book.startBorrow = max([start_date, datetime.now()])
    else:
        borrow_book.startBorrow = datetime.now()
    if end_date == None:
        end = datetime.now() + timedelta(days=int(borrow_time))
    elif end_date != None and end_date < start_date:
        return False, None, INVALID_DURATION
    else:
        borrow_book.endBorrow = end_date

    user = db.session.query(User).filter(User.id == userId).all()
    book = db.session.query(Book).filter(Book.id == bookId).all()

    if not user or not book:
        return False, None, INVALID_ID #No user or book with that ID exists
    
    borrow_book.bookId = bookId
    borrow_book.userId = userId
    borrow_book.hasReturned = False
    
    try:
        db.session.add(borrow_book)
        db.session.commit()
        return True, borrow_book, None
    except:
        db.session.rollback()
        return False, None, EDIT_ERROR

def edit_borrow(borrow_id: int, userId: int=None, bookId: int=None, start_date: datetime=None, end_date: datetime=None, has_returned: bool=False, return_date: datetime=None, damaged_or_lost: bool=None):
    borrow_book = db.session.query(BookBorrow).filter(BookBorrow.id == borrow_id).first()
    if not borrow_book:
        return False, None, ROW_NOT_EXISTS
    
    if start_date != None:
        borrow_book.startBorrow = start_date

    if end_date != None and end_date < start_date:
        return False, None, INVALID_DURATION
    else:
        borrow_book.endBorrow = end_date

    if return_date != None and return_date < start_date:
        return False, None, INVALID_DURATION
    else:
        borrow_book.returnDate = return_date
    if userId != None:
        user = db.session.query(User).filter(User.id == userId).first()
        if not user:
            return False, None, INVALID_ID #No user or book with that ID exists
    if bookId != None:
        book = db.session.query(Book).filter(Book.id == bookId).first()
        if not book:
            return False, None, INVALID_ID #No user or book with that ID exists

    
    if bookId != None:
        borrow_book.bookId = bookId
    if userId != None:
        borrow_book.userId = userId
    borrow_book.hasReturned = has_returned
    
    if damaged_or_lost != None:
        borrow_book.isDamagedOrLost = damaged_or_lost

    try:
        db.session.add(borrow_book)
        db.session.commit()
        return True, borrow_book, None
    except:
        db.session.rollback()
        return False, None, EDIT_ERROR

def return_book(userId: int, id: int, damagedOrLost: bool=False):
    borrow_book = db.session.query(BookBorrow).filter(BookBorrow.userId == userId) \
        .filter(BookBorrow.id == id).first()
    if borrow_book != None:
        borrow_book.hasReturned = True
        borrow_book.returnDate = datetime.now()
        borrow_book.isDamagedOrLost = damagedOrLost
        try:
            db.session.commit()
            return True, borrow_book, None
        except:
            db.session.rollback()
            return False, None, EDIT_ERROR

def get_borrow_book(userId: int, get_returned:bool = False):
    query = select(BookBorrow).filter(BookBorrow.userId == userId)
    if get_returned == False:
        query.filter(BookBorrow.hasReturned == False)
    
    result = db.session.execute(query)
    result = result.all()
    result = [query_result[0] for query_result in result]
    return True, result, None

def search_borrow(userId: int=None, bookId: int=None, start_date: datetime = None, end_date: datetime=None, get_returned: bool=True, page: int = None, limit: int=None):
    query = select(BookBorrow)
    if userId != None:
        query.filter(BookBorrow.userId == userId)
    if bookId != None:
        query.filter(BookBorrow.bookId == bookId)
    if start_date != None:
        query.filter(BookBorrow.startBorrow >= start_date)
    if end_date != None:
        query.filter(BookBorrow.endBorrow <= end_date)
    if page != None and limit != None and page >= 1 and limit >= 1:
        offset = (page - 1) * limit
        print(offset)
        query.offset(offset).limit(limit)
    query.filter(BookBorrow.hasReturned == get_returned)

    result = db.session.execute(query)
    result = result.all()
    result = [query_result[0] for query_result in result]
    return True, result, None

def delete_borrow(borrow_id: int):
    try:
        delete_status = db.session.query(BookBorrow).filter(BookBorrow.id == borrow_id).delete()
        db.session.commit()
        return True, delete_status, None
    except:
        db.session.rollback()
        return False, None, DELETE_ERROR

#Args:
# other_fees: Other fees that is included (such as borrowing fees, fines for recoverable book damages, book's prices for damaged/lost borrows,...)
def get_borrow_fee(borrow_id: int, other_fees: float):
    borrow = db.session.query(BookBorrow).filter(BookBorrow.id == borrow_id).first()

    if not borrow:
        return False, None, INVALID_ID
    
    is_damaged_or_lost = borrow.isDamagedOrLost
    end_borrow = borrow.endBorrow
    return_date = borrow.returnDate

    if borrow.hasReturned == False or return_date == None:
        #Haven't return the book yet
        return False, None, BOOK_NOT_RETURNED

    time_difference = return_date - end_borrow
    #If return date is before end borrowing date, or overdue under 12 hours
    if return_date <= end_borrow or ((return_date > end_borrow) 
                                     and time_difference.days == 0 and time_difference.seconds / 3600 < 12):
        overdue = 0
    else:
        overdue = max(time_difference.days, 1)

    total = 0.0
    if overdue <= int(overdue_limit_before_treated_as_lost):
        total = float(overdue) * float(overdue_fine)
    #If the book is irrecoverably damaged or lost
    if is_damaged_or_lost or overdue > int(overdue_limit_before_treated_as_lost):
        total += damage_and_lost_fine 
    
    total += other_fees
    return True, total, None



def add_favorite(userId: int, bookId: int):
    user = db.session.query(User).filter(User.id == userId).first()
    book = db.session.query(Book).filter(Book.id == bookId).first()
    if not user or not book:
        return False, None, ADD_ENTRY_ERROR
    else:
        favorite = BookFavorite()
        favorite.userId = userId
        favorite.bookId = bookId
        db.session.add(favorite)
        db.session.commit()
        return True, favorite, None

def remove_favorite(userId: int, bookId: int, favoriteId: int):
    user = db.session.query(User).filter(User.id == userId).first()
    book = db.session.query(Book).filter(Book.id == bookId).first()
    if not user or not book:
        return False, None, ADD_ENTRY_ERROR
    else:
        rows_deleted = db.session.query(BookFavorite).filter(BookFavorite.userId == userId).filter(BookFavorite.bookId == bookId) \
            .filter(BookFavorite.id == favoriteId).delete()
        db.session.commit()
        return True, rows_deleted, None

def does_book_have_ebook(bookId: int):
    bookpdf = db.session.query(BookFile).filter(bookId == BookFile.bookId).all()
    if bookpdf == None or len(bookpdf) == 0:
        return False
    else:
        return True


def get_ebook(bookId: int):
    bookpdf = db.session.query(BookFile).filter(bookId == BookFile.bookId).all()
    return bookpdf