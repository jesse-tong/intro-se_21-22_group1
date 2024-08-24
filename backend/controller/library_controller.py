import sqlite3
from global_vars.errors import *
from dataclasses import asdict
from dateutil.parser import ParserError
from global_vars.constants import *
from global_vars.database_init import policies_db_path
from utils.time_utils import sqlite_time_string_from_time_string as time_to_sqlite
from controller.user_controller import get_current_user_role
from models.library_misc import Article
from models.book_model import Book
from global_vars.database_init import db
from utils.file_utils import *
from utils.get_status_object import convert_sqlalchemy_row
from sqlalchemy import desc, asc, or_


def update_policies(default_borrow_time: int=None, overdue_fine_per_day: float=None, 
                    overdue_limit: int=None, damage_lost_fine: float = None, new_currency: str=None, other_policies: str=None):
    success, role, error = get_current_user_role()
    if success == False or role != 'admin':
        return get_current_user_role(False, None, NOT_AUTHENTICATED)
    
    query = 'UPDATE LIB_POLICIES SET {} WHERE ID = 1'
    set_str = []
    if default_borrow_time != None:
        set_str.append('DEFAULT_BORROW_TIME = ' + str(default_borrow_time))
    if overdue_fine_per_day != None:
        set_str.append('OVERDUE_FEE = ' + str(overdue_fine_per_day))
    if overdue_limit != None:
        set_str.append('OVERDUE_LIMIT = ' + str(overdue_limit))
    if damage_lost_fine != None:
        set_str.append('DAMAGE_AND_LOST_FEE = ' + str(damage_lost_fine))
    if new_currency != None:
        set_str.append("CURRENCY = '{}'".format(str(new_currency)))
    if other_policies != None:
        set_str.append("OTHER_POLICIES = ?")

    query = query.format(', '.join(set_str))
    with sqlite3.connect(policies_db_path) as connection:
        try:
            if other_policies != None:
                connection.execute(query, (str(other_policies),))
            else:
                connection.execute(query)
            connection.commit()
        except sqlite3.Error as er:
            return False, er.sqlite_errorcode
    
    return True, None

def update_library_contacts(address: str=None, phone_number: str=None, email: str=None):
    success, role, error = get_current_user_role()
    if success == False or role != 'admin':
        return get_current_user_role(False, None, NOT_AUTHENTICATED)
    
    query = 'UPDATE LIB_CONTACTS SET {} WHERE ID = 1'
    set_str = []

    if address != None:
        set_str.append("ADDRESS = '{}'".format(str(address)))
    if phone_number != None:
        set_str.append("PHONE_NUMBER = '{}'".format(str(phone_number)))
    if email != None:
        set_str.append("EMAIL = '{}'".format(str(email)))

    query = query.format(', '.join(set_str))
    with sqlite3.connect(policies_db_path) as connection:
        try:
            connection.execute(query)
            connection.commit()
        except sqlite3.Error as er:
            return False, er.sqlite_errorcode
    
    return True, None

def get_policies():
    with sqlite3.connect(policies_db_path) as connection:
        try:
            policies = connection.execute('SELECT * FROM LIB_POLICIES WHERE ID = 1').fetchone()
            return policies
        except:
            return None
        
def get_library_contacts():
    with sqlite3.connect(policies_db_path) as connection:
        try:
            contacts = connection.execute('SELECT * FROM LIB_CONTACTS WHERE ID = 1').fetchone()
            return contacts
        except:
            return None
        
def get_library_timings():
    with sqlite3.connect(policies_db_path) as connection:
        try:
            timings = connection.execute('SELECT * FROM LIB_TIMINGS WHERE ID = 1').fetchone()
            return timings
        except:
            return None
        
def update_timings(normal_day_open: str=None, normal_day_close: str=None, weekend_open: str=None, weekend_close: str=None, 
                    weekend_start: int=None, weekend_end: int=None):
    success, role, error = get_current_user_role()
    if success == False or role != 'admin':
        return get_current_user_role(False, None, NOT_AUTHENTICATED)
    
    query = 'UPDATE LIB_TIMINGS SET {} WHERE ID = 1'
    set_str = []

    current_timings = get_library_timings() #Get current timings
    if current_timings != None:
        #Weekend start and end after update
        new_weekend_start = int(current_timings[-2]) if weekend_start == None else weekend_start
        new_weekend_end = int(current_timings[-1]) if weekend_end == None else weekend_end

    try:
        if normal_day_open != None:
            normal_day_open = time_to_sqlite(normal_day_open)
            set_str.append("NORMAL_OPEN = '{}'".format(str(normal_day_open)))
        if normal_day_close != None:
            normal_day_close = time_to_sqlite(normal_day_close)
            set_str.append("NORMAL_CLOSE = '{}'".format(str(normal_day_close)))
        if weekend_open != None:
            weekend_open = time_to_sqlite(weekend_open)
            set_str.append("WEEKEND_OPEN = '{}'".format(str(weekend_open)))
        if weekend_close != None:
            weekend_close = time_to_sqlite(weekend_close)
            set_str.append("WEEKEND_CLOSE = '{}'".format(str(weekend_close)))
    except ParserError:
        return False, INVALID_PARAM

    if weekend_start != None:
        if weekend_start <= 1 or weekend_start > 8:
            return False, INVALID_PARAM
        set_str.append('WEEKEND_START = ' + str(weekend_start))
    if weekend_end != None:
        if weekend_end <= 1 or weekend_end > 8:
            return False, INVALID_PARAM
        set_str.append('WEEKEND_END = ' + str(weekend_end))
    
    if new_weekend_start != None and new_weekend_end != None and new_weekend_start > new_weekend_end:
        return False, INVALID_DURATION #Case of weekend after updating is invalid

    query = query.format(', '.join(set_str))
    with sqlite3.connect(policies_db_path) as connection:
        try:
            connection.execute(query)
            connection.commit()
        except sqlite3.Error as er:
            return False, str(er.sqlite_errorname)
    
    return True, None

def add_article(title: str, content: str, category: str = None):
    get_role_success, role, error  = get_current_user_role()
    if role != 'admin':
        return get_role_success, None, error
    
    try:
        new_article = Article(); 
        new_article.title = title; new_article.content = content
        new_article.category = category
        db.session.add(new_article); db.session.commit()
    except:
        return False, None, DATABASE_ERROR
    return True, new_article, None

def edit_article(article_id: int, title: str, content: str, category: str = None):
    get_role_success, role, error  = get_current_user_role()
    if role != 'admin':
        return False, None, INVALID_AUTH
    
    #try:
    new_article = db.session.query(Article).filter(Article.id == article_id).first()
    new_article.title = title; new_article.content = content; new_article.category = category
    db.session.commit()
    #except:
    #    return False, None, DATABASE_ERROR
    return True, new_article, None

def delete_article(id: int):
    try:
        row_deleted = db.session.query(Article).filter(Article.id == id).delete()
        db.session.commit()
        return True, None, None
    except:
        return False, None, DATABASE_ERROR

def get_article(id: int):
    article = db.session.query(Article).filter(Article.id == id).first()
    return True, article, None

def get_article_summaries(page: int=None, limit: int = 6, descending=True):
    if page !=None and limit != None and (page < 1 or limit <= 0):
        return False, None, INVALID_PARAM
    
    if page != None and limit != None:
        offset = (page - 1)*limit
    query = db.session.query().with_entities(Article.id, Article.title, Article.category, Article.date) \
                                .group_by(Article.id, Article.date)
    
    if descending == True:
        query = query.order_by(desc(Article.date))
    else:
        query = query.order_by(asc(Article.date))

    if page != None and limit != None:
        article_summaries = query.offset(offset).limit(limit).all()
    else:
        article_summaries = query.all()
    
    article_summaries = [convert_sqlalchemy_row(article) for article in article_summaries]
    return True, article_summaries, None

def search_everything_controller(query: str):
    query = '%' + query + '%'
    articles = db.session.query(Article).filter(or_(Article.title.ilike(query), Article.content.ilike(query))).all()
    books = db.session.query(Book).filter(or_(Book.title.ilike(query), Book.description.ilike(query))).all()
    
    return { 'articles' :articles, 'books': books }