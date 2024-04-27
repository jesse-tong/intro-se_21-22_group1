from werkzeug.security import generate_password_hash, check_password_hash
from models.user_model import User
from models.book_model import Book, BookFile
from models.user_book import BookBorrow, BookFavorite
from sqlalchemy import select, func, desc
from global_vars.database_init import db
from global_vars.errors import *
from datetime import datetime, timedelta, timezone
from dateutil.parser import parse as dateparse
from global_vars.constants import *
from global_vars.init_env import *
from dataclasses import asdict
from controller.book_controller import increment_book_stock, decrement_book_stock, is_book_out_of_stock
borrow_time = os.environ.get('DEFAULT_BORROW_TIMEOUT')
overdue_fine = os.environ.get('OVERDUE_FINE_PER_DAY')
overdue_limit_before_treated_as_lost = os.environ.get('OVERDUE_DAYS_LIMIT_BEFORE_LOST')
damage_and_lost_fine = os.environ.get('DAMAGE_AND_LOST_FINE')


#Default if start_date is null is the current date
def borrow_book(userId: int, bookId: int, start_date: datetime=None, end_date: datetime=None, do_not_decrement_book_stock: bool=False):
    borrow_book = BookBorrow()
    if start_date != None:
        borrow_book.startBorrow = max([start_date, datetime.now(timezone.utc)])
    else:
        borrow_book.startBorrow = datetime.now()
    if end_date == None:
        end = datetime.now() + timedelta(days=int(borrow_time))
        borrow_book.endBorrow = end
    elif end_date != None and end_date < start_date:
        return False, None, INVALID_DURATION
    else:
        borrow_book.endBorrow = end_date

    user = db.session.query(User).filter(User.id == userId).all()
    book = db.session.query(Book).filter(Book.id == bookId).all()

    if not user or not book:
        return False, None, INVALID_ID #No user or book with that ID exists
    
    if is_book_out_of_stock(bookId) == True:
        return False, None, BOOK_OUT_OF_STOCK

    borrow_book.bookId = bookId
    borrow_book.userId = userId
    borrow_book.hasReturned = False
    
    try:
        db.session.add(borrow_book)
        db.session.commit()
        decrement_book_stock(bookId)
        return True, borrow_book, None
    except:
        db.session.rollback()
        return False, None, EDIT_ERROR

def edit_borrow(borrow_id: int, userId: int=None, bookId: int=None, start_date: datetime=None, end_date: datetime=None, has_returned: bool=False, 
                return_date: datetime=None, damaged_or_lost: bool=None, is_approved: bool=None):
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
    prev_return_state = borrow_book.hasReturned
    borrow_book.hasReturned = has_returned
    
    previous_book_status = borrow_book.isDamagedOrLost
    if damaged_or_lost != None:
        borrow_book.isDamagedOrLost = damaged_or_lost
    new_book_status = damaged_or_lost

    is_old_status_restockable =  (prev_return_state == True and previous_book_status == False)

    if is_old_status_restockable == True and ((prev_return_state != has_returned and has_returned == False) or 
        (previous_book_status != new_book_status and new_book_status == True)):
        #New book status change to being damaged/lost, or return state change from has returned to not returned
        # => reduce book stock
        decrement_book_stock(bookId)
    elif is_old_status_restockable == False and((prev_return_state != has_returned and has_returned == True and new_book_status == False) or 
    (has_returned == True and previous_book_status != new_book_status and new_book_status == False)):
        #If new book status change from being damaged/lost to be being usable and has been returned,
        #or the book change from being borrowed to being returned and still being usable => increase book stock
        increment_book_stock(bookId)
    if is_approved != None:
        borrow_book.isApproved = is_approved
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
        has_returned = borrow_book.hasReturned
        is_approved = borrow_book.isApproved
        if has_returned:
            return False, None, BOOK_HAS_RETURNED
        if not is_approved:
            return False, None, BORROW_NOT_APPROVED
        
        borrow_book.hasReturned = True
        borrow_book.returnDate = datetime.now()
        borrow_book.isDamagedOrLost = damagedOrLost
        if damagedOrLost == False:
            increment_book_stock(borrow_book.bookId)

        try:
            db.session.commit()
            return True, borrow_book, None
        except:
            db.session.rollback()
            return False, None, EDIT_ERROR

def get_borrow_book(userId: int, get_returned:bool = False):
    query = select(BookBorrow).filter(BookBorrow.userId == userId)
    if get_returned == False:
        query = query.filter(BookBorrow.hasReturned == False)
    
    result = db.session.execute(query)
    result = result.all()
    result = [query_result[0] for query_result in result]
    return True, result, None

def search_borrow(user_id: int=None, book_id: int=None, start_date: datetime = None, end_date: datetime=None, get_returned: bool=True, page: int = None, limit: int=None):
    query = db.session.query(BookBorrow)

    if user_id != None:
        query = query.filter(BookBorrow.userId == user_id)
    if book_id != None:
        query = query.filter(BookBorrow.bookId == book_id)
    if start_date != None:
        query = query.filter(BookBorrow.startBorrow >= start_date)
    if end_date != None:
        query = query.filter(BookBorrow.endBorrow <= end_date)
    
    if get_returned == False:
        query = query.filter(BookBorrow.hasReturned == False)
    if page != None and limit != None and page >= 1 and limit >= 1:
        offset = (page - 1) * limit
        query = query.offset(offset).limit(limit)

    result = query.all()
    return_obj = list()
    for borrow in result:
        borrow_dict = asdict(borrow)
        success, fee, error = calculate_fee(borrow, 0.0)
        borrow_dict['fee'] = fee
        return_obj.append(borrow_dict)

    return True, return_obj, None

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
    return calculate_fee(borrow, other_fees)

def calculate_fee(borrow, other_fees):
    is_damaged_or_lost = borrow.isDamagedOrLost
    end_borrow = borrow.endBorrow
    return_date = borrow.returnDate

    if borrow.hasReturned == False or return_date == None:
        #Haven't return the book yet
        return False, 0.0, BOOK_NOT_RETURNED
    
    if borrow.isApproved == False:
        #Borrow haven't been approved yet
        return False, 0.0, BORROW_NOT_APPROVED 

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
        total += float(damage_and_lost_fine)
    
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
    
def toggle_favourite(userId: int, bookId: int):
    favourite = db.session.query(BookFavorite).filter(BookFavorite.userId == userId).filter(BookFavorite.bookId == bookId).first()
    if favourite != None:
        favorite = BookFavorite()
        favorite.userId = userId
        favorite.bookId = bookId
        db.session.add(favorite)
        try:
            db.session.commit()
            return True, favorite, None
        except:
            db.session.rollback()
            return False, None, DATABASE_ERROR
    else:
        favoriteId = favourite.id
        rows_deleted = db.session.query(BookFavorite).filter(BookFavorite.userId == userId).filter(BookFavorite.bookId == bookId) \
            .filter(BookFavorite.id == favoriteId).delete()
        try:
            db.session.commit()
            return True, rows_deleted, None
        except:
            db.session.rollback()
            return False, None, DATABASE_ERROR
        


def does_book_have_ebook(bookId: int):
    bookpdf = db.session.query(BookFile).filter(bookId == BookFile.bookId).all()
    if bookpdf == None or len(bookpdf) == 0:
        return False
    else:
        return True


def get_ebook(bookId: int):
    bookpdf = db.session.query(BookFile).filter(bookId == BookFile.bookId).all()
    return bookpdf

#This will get like (a number) of books that other users that borrow this book also borrow the most
#Query: select b.bookId, count(b.bookId) as count_borrow from bookborrow b 
#       where b.userId in (select distinct b2.userId from bookborrow b2 where b2.bookId = 4) 
#       group by b.bookId order by count(b.bookId) desc limit 10
def get_related_books_others_borrow_most(book_id: int):
    subquery = db.session.query(BookBorrow.userId).filter(BookBorrow.bookId == book_id).subquery()
    result = db.session.query(BookBorrow.bookId, func.count(BookBorrow.bookId)).filter(BookBorrow.userId.in_(subquery)).group_by(BookBorrow.bookId) \
        .order_by(desc(BookBorrow.bookId)).limit(10).all()
    return True, result, None
