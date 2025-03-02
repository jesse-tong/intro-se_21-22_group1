from werkzeug.security import generate_password_hash, check_password_hash
from models.user_model import User
from models.book_model import Book, BookFile
from models.user_book import BookBorrow, BookFavorite
from models.user_model import Comment
from sqlalchemy import select, func, desc, distinct
from global_vars.database_init import db
from global_vars.errors import *
from datetime import datetime, timedelta, timezone
from dateutil.parser import parse as dateparse
from global_vars.constants import *
from global_vars.init_env import *
from controller.library_controller import update_policies, get_policies
from dataclasses import asdict
from flask_login import current_user
from controller.user_controller import check_user_authentication
from threading import Thread, Lock
from controller.book_controller import increment_book_stock, decrement_book_stock, is_book_out_of_stock

try:
    library_policies = get_policies()
    if library_policies != None:
        id, borrow_time, overdue_fine, overdue_limit_before_treated_as_lost, \
            damage_and_lost_fine, currency, other_policies = library_policies
except:
    raise ValueError('Error getting variables in the library policies database, please check the server.')

env_lock = Lock()

def get_borrow_policy_constants(no_policy_text=False):
    if no_policy_text == True:
        result = { 'overdue_fine': overdue_fine, 'overdue_time_limit': overdue_limit_before_treated_as_lost, 
              'damage_and_lost_fine': damage_and_lost_fine, 'currency': currency}
    else:
        result = { 'overdue_fine': overdue_fine, 'overdue_time_limit': overdue_limit_before_treated_as_lost, 
              'damage_and_lost_fine': damage_and_lost_fine, 'currency': currency, 'other_policies': other_policies}
    return True, result, None

#Default if start_date is null is the current date
def borrow_book(userId: int, bookId: int, start_date: datetime=None, end_date: datetime=None, 
                is_approved: bool=False, return_date: datetime=None, is_damaged_or_lost: bool=False, 
                has_resolved: bool = False, renew_pending: bool = False, do_not_decrement_book_stock: bool=False):
    borrow_book = BookBorrow()
    if start_date != None:
        borrow_book.startBorrow = start_date
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
    borrow_book.isApproved = is_approved
    borrow_book.isDamagedOrLost = is_damaged_or_lost
    borrow_book.hasResolved = has_resolved
    borrow_book.renewPending = renew_pending

    if return_date != None and return_date < start_date:
        return False, None, INVALID_DURATION
    else:
        borrow_book.returnDate = return_date
    
    if borrow_book.returnDate != None:
        borrow_book.hasReturned = True


    try:
        db.session.add(borrow_book)
        db.session.commit()
        if borrow_book.hasReturned == False or borrow_book.isDamagedOrLost == True:
            decrement_book_stock(bookId)
        return True, borrow_book, None
    except:
        db.session.rollback()
        return False, None, EDIT_ERROR

def edit_borrow(borrow_id: int, userId: int=None, bookId: int=None, start_date: datetime=None, end_date: datetime=None, has_returned: bool=False, 
                return_date: datetime=None, damaged_or_lost: bool=None, is_approved: bool=None, has_resolved: bool=None, renew_pending: bool=None): 
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

    if has_resolved != None:
        borrow_book.hasResolved = bool(has_resolved)

    if renew_pending != None:
        borrow_book.renewPending = bool(renew_pending)

    prev_return_state = borrow_book.hasReturned
    borrow_book.hasReturned = has_returned
    new_return_state = borrow_book.hasReturned
    
    prev_damage_lost_status = borrow_book.isDamagedOrLost
    if damaged_or_lost != None:
        borrow_book.isDamagedOrLost = damaged_or_lost
    new_damage_lost_status = damaged_or_lost

    prev_approve_state = borrow_book.isApproved
    if is_approved != None:
        borrow_book.isApproved = is_approved
    new_approve_state = borrow_book.isApproved

    #Restockable mean a book has been returned and not irrecoverable damaged/lost
    prev_status_restockable =  (prev_return_state == True and prev_damage_lost_status == False)
    new_status_restockable =  (new_return_state == True and new_damage_lost_status == False)

    #We have four scenarios for changing borrow status
    # unapproved -> approved & not restockable (either not returned or returned but damaged/lost) -1
    # approved & not restockable -> unapproved       +1
    # approved & not restockable -> approved & restockable     +1
    # approved & restockable -> approved & not restockable     -1
    
    if prev_approve_state == False and new_approve_state == True and new_status_restockable == False:
        db.session.query(Book).filter(Book.id == bookId).update({Book.stock: Book.stock - 1})

    if prev_approve_state == True and prev_status_restockable == False and new_approve_state == False:
        db.session.query(Book).filter(Book.id == bookId).update({Book.stock: Book.stock + 1})

    if prev_approve_state == True and prev_status_restockable == False and new_approve_state == True and new_status_restockable == True:
        db.session.query(Book).filter(Book.id == bookId).update({Book.stock: Book.stock + 1})

    if prev_approve_state == True and prev_status_restockable == True and new_approve_state == True and new_status_restockable == False:
        db.session.query(Book).filter(Book.id == bookId).update({Book.stock: Book.stock - 1})

    try:
        db.session.commit()
        return True, borrow_book, None
    except:
        db.session.rollback()
        return False, None, EDIT_ERROR

def renew_borrow(userId: int, borrow_id: int, new_end_date: int):
    #new_end_date: number of days to extend the borrow
    borrow_book = db.session.query(BookBorrow).filter(BookBorrow.userId == userId) \
        .filter(BookBorrow.id == borrow_id).first()
    if borrow_book != None:
        if borrow_book.hasReturned:
            return False, None, BOOK_HAS_RETURNED
        if not borrow_book.isApproved:
            return False, None, BORROW_NOT_APPROVED
        borrow_book.endBorrow = borrow_book.endBorrow + timedelta(days=new_end_date)
        borrow_book.returnDate = None; borrow_book.hasReturned = False; borrow_book.isApproved = False
        borrow_book.renewPending = True
        try:
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

def set_borrow_resolve(borrow_id: int):
    try:
        updated_count = db.session.query(BookBorrow).filter(BookBorrow.id == borrow_id).update({BookBorrow.hasResolved: True})
        db.session.commit()
        return True, updated_count, None
    except:
        return False, None, DATABASE_ERROR

def delete_borrow(borrow_id: int):
    borrow = db.session.query(BookBorrow).filter(BookBorrow.id == borrow_id).first()
    if borrow != None:
        #If the borrow request is not approved, increase the book stock
        if borrow.isApproved == False:
            db.session.query(Book).filter(Book.id == borrow.bookId).update({Book.stock: Book.stock + 1})
        elif borrow.hasReturned and not borrow.isDamagedOrLost: #Book has been returned and no irrecoverable damage or lost
            db.session.query(Book).filter(Book.id == borrow.bookId).update({Book.stock: Book.stock + 1})
        elif borrow.hasReturned and borrow.isDamagedOrLost: #Book has been returned and with irrecoverable damage or the book has been lost
            #Since after borrowing the stock has already decremented by 1
            db.session.query(Book).filter(Book.id == borrow.bookId).update({Book.stock: Book.stock})
        else:
            return False, None, BOOK_NOT_RETURNED_NOT_DELETABLE
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
        favorite = db.session.query(BookFavorite).filter(BookFavorite.bookId == bookId) \
        .filter(BookFavorite.userId == userId).first()
        if favorite:
            return True, favorite, None
        favorite = BookFavorite()
        favorite.userId = userId
        favorite.bookId = bookId
        db.session.add(favorite)
        db.session.commit()
        return True, favorite, None

def remove_favorite(userId: int, bookId: int):
    user = db.session.query(User).filter(User.id == userId).first()
    book = db.session.query(Book).filter(Book.id == bookId).first()
    if not user or not book:
        return False, None, ADD_ENTRY_ERROR
    else:
        rows_deleted = db.session.query(BookFavorite).filter(BookFavorite.userId == userId).filter(BookFavorite.bookId == bookId).delete()
        db.session.commit()
        return True, rows_deleted, None
    
def toggle_favourite(userId: int, bookId: int):
    favourite = db.session.query(BookFavorite).filter(BookFavorite.userId == userId).filter(BookFavorite.bookId == bookId).first()
    if favourite == None:
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
        
def get_favorite(bookId: int):
    is_user_mark_book_favorite = None
    if check_user_authentication() == True:
        favourite = db.session.query(BookFavorite).filter(BookFavorite.userId == current_user.id).filter(BookFavorite.bookId == bookId).first()
        if favourite != None:
            is_user_mark_book_favorite = True
        else:
            is_user_mark_book_favorite = False
    
    favourite_count_for_book = db.session.query(func.count(distinct(BookFavorite.userId))).filter(BookFavorite.bookId == bookId).first()[0]
    return True, { 'favorite_count': favourite_count_for_book, 'is_book_favorite_by_user': is_user_mark_book_favorite },None

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
    subquery = db.session.query(BookBorrow.userId).filter(BookBorrow.bookId == book_id)
    result = db.session.query(Book, BookBorrow.bookId, func.count(BookBorrow.bookId)).filter(BookBorrow.userId.in_(subquery)).group_by(BookBorrow.bookId) \
        .order_by(desc(BookBorrow.bookId)).join(Book, Book.id == BookBorrow.bookId).limit(10).all()
    return True, result, None

def group_borrow_by_start_borrow_month():
    result = db.session.query(func.month(BookBorrow.startBorrow), func.year(BookBorrow.startBorrow), func.count(BookBorrow.id))\
   .group_by(func.year(BookBorrow.startBorrow), func.month(BookBorrow.startBorrow))\
   .order_by(desc(func.year(BookBorrow.startBorrow)), desc(func.month(BookBorrow.startBorrow))).limit(24).all()
    
    result = [{'month': obj[0], 'year':obj[1], 'borrow_count': obj[2]} for obj in result]
    return True, result, None

def get_highest_rated_books(limit: int=15):
    result = db.session.query(Book).join(Comment, Book.id == Comment.bookId).group_by(Book.id) \
            .order_by(desc(func.avg(Comment.rating))).limit(limit).all()
    return True, result, None

def most_borrowed_books(limit: int=15):
    result = db.session.query(Book).join(BookBorrow, BookBorrow.bookId == Book.id).group_by(Book.id) \
            .order_by(desc(func.count(BookBorrow.id))).limit(limit).all()
    return True, result, None

def most_recent_borrows(limit: int=10):
    result = db.session.query(BookBorrow, User.name, Book.title).join(User, BookBorrow.userId == User.id).join(Book, BookBorrow.bookId == Book.id) \
    .group_by(BookBorrow.id).order_by(desc(BookBorrow.startBorrow)).limit(limit).all()
    result = [asdict(item[0]) |{'username': item[1], 'title': item[2] } for item in result]
    return True, result, None

def set_library_policies_controller(default_borrow_time: int=None, overdue_fine_per_day: float=None, overdue_limit: int=None, damage_lost_fine: float = None, new_currency: str=None, new_other_policies: str=None):
    global id, borrow_time, overdue_fine, overdue_limit_before_treated_as_lost, damage_and_lost_fine, currency, other_policies
    with env_lock:
        success, error_code = update_policies(default_borrow_time, overdue_fine_per_day, overdue_limit, damage_lost_fine, new_currency, new_other_policies)
        if success == True:
            library_policies = get_policies()
            global id, borrow_time, overdue_fine, overdue_limit_before_treated_as_lost, \
            damage_and_lost_fine, currency, other_policies
            id, borrow_time, overdue_fine, overdue_limit_before_treated_as_lost, \
            damage_and_lost_fine, currency, other_policies = library_policies
            
    result = { 'overdue_fine': overdue_fine, 'overdue_time_limit': overdue_limit_before_treated_as_lost, 'damage_and_lost_fine': damage_and_lost_fine, 
              'currency': currency, 'other_policies': other_policies}
    return True, result, None

