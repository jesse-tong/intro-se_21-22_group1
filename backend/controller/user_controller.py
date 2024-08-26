from werkzeug.security import generate_password_hash, check_password_hash
from models.user_model import User, UserInfo, UserNotification, Session
from models.user_book import BookBorrow, BookFavorite
from models.library_misc import MonthlySessionCount
from sqlalchemy import func, update, case
from sqlalchemy.dialects.mysql import insert as mysql_insert
from global_vars.database_init import db
from utils.email_utils import send_verification_email
import re, jwt, datetime
from datetime import timezone
from ua_parser import user_agent_parser
from global_vars.errors import *
from flask_login import login_user, login_required, current_user, logout_user

def check_user_authentication():
    return current_user.is_authenticated and current_user.isRestricted == False

async def register(email: str, password: str, name: str, role: str, resend_verification_email=False):

    user = User.query.filter_by(email = email).first()
    if (user and resend_verification_email == False):
        return False, None, EMAIL_EXISTS
    
    #Reference: https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    if re.fullmatch(email_regex, email) == None:
        return False, None, INVALID_EMAIL

    if resend_verification_email != None:
        new_user = User(email = email, name = name, role = role, password = generate_password_hash(password=password))
    else:
        new_user = db.session.query(User).filter(User.email == email, User.name == name).first()

    if resend_verification_email == False:
        try:
            db.session.add(new_user)
            db.session.commit()
            print(resend_verification_email)
            token = jwt.encode(payload={ 'id': new_user.id, 'email': email, 'name': name, 'role': role, 
                                        "exp": datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(seconds=3600) }, key="my_secret_key")
            try:
                await send_verification_email(token, email)
            except:
                return False, new_user, SEND_VERIFICATION_EMAIL_FAILED
            
            return True, new_user, None
        except:
            db.session.rollback()
            return False, None, ADD_ENTRY_ERROR
    else:
        token = jwt.encode(payload={ 'id': new_user.id, 'email': email, 'name': name, 'role': role, 
                                    "exp": datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(seconds=3600) }, key="my_secret_key", algorithm='HS256')
        try:
            await send_verification_email(token, email)
        except: 
            return False, None, 'Resend verification email failed!'
        return True, new_user, None

def verify_email_address(token):
    try:
        payload = jwt.decode(token, key="my_secret_key", algorithms=['HS256'], leeway=60.0)
    except:
        return False, None, INVALID_AUTH
    if payload != None and payload.get('id') and payload.get('email'):
        user = db.session.query(User).filter(User.id == int(payload.get('id'))).filter(User.email == str(payload.get('email'))).first()
        user.isVerified = True
        db.session.commit()
        return True, None, None
    else:
        return False, None, INVALID_AUTH
    

#Return true if userId not exists or is restricted, false for others
def isRestricted(userId: int):
    user = db.session.query(User).filter(User.id == id).first()
    if not user:
        return True
    elif user.isRestricted == True:
        return True
    else:
        return False

def login(email: str, password: str, remember: bool):
    user = User.query.filter_by(email = email).first()
    if not user or not check_password_hash(user.password, password):
        return False, None, INVALID_AUTH
    
    if user.isRestricted == True:
        return False, None, INVALID_AUTH

    login_user(user, remember=remember)
    return True, user, None

#Note that this function will only allow you to change password if you have been logged in
#I may make a function to recover lost password later though
def change_password(old_password, new_password):
    if not check_user_authentication():
        return False, None, NOT_AUTHENTICATED
    
    user = db.session.query(User).filter(User.id == current_user.id).first()
    if not user or (user.password != None and not (check_password_hash(user.password, old_password))):
        return False, None, INVALID_AUTH
    else:
        new_password_hash = generate_password_hash(new_password)
        user.password = new_password_hash
        db.session.commit()
        logout_user()
        return True, user, None

def get_current_user_role():
    if not check_user_authentication():
        return False, None, NOT_AUTHENTICATED
    user_id = current_user.id
    user = db.session.query(User).filter(User.id == user_id).first()

    if user == None:
        return False, None, USER_NOT_EXIST
    else:
        return True, user.role, None
    
def add_update_user_infos(user_id: int, age: int = None, gender: str = None, borrowMax: int=5, phone: str = None, address: str = None):
    add_new = False
    user_infos = db.session.query(UserInfo).filter(UserInfo.userId == user_id).first()
    if user_infos == None:
        add_new = True
        user_infos = UserInfo()
        user_infos.borrowLeft = borrowMax

    if (borrowMax !=None and borrowMax < 0):
        return False, None, INVALID_PARAM
    #Phone should have from 8-15 number characters
    if phone != None and not re.match(r'[\+\-0-9]{8,15}', phone):
        return False, None, 'Invalid phone number'
    user_infos.userId = user_id

    if user_infos.borrowLeft == user_infos.maxBorrow:
        user_infos.borrowLeft = borrowMax
        
    user_infos.age = age; user_infos.gender = gender; user_infos.maxBorrow = borrowMax
    user_infos.phone = phone; user_infos.address = address

    try:
        if add_new == True:
            db.session.add(user_infos)
        db.session.commit()
        return True, user_infos, None
    except:
        db.session.rollback()
        return False, None, EDIT_ERROR

def user_profile(user_id: int):
    profile = db.session.query(User, UserInfo).join(UserInfo, User.id == UserInfo.userId, isouter=True).filter(User.id == user_id).first()
    return True, profile, None


def send_notification(to_user: int, notification_data: str):
    user = db.session.query(User).filter(User.id == to_user).first()
    if not user:
        return False, None, USER_NOT_EXIST

    new_notification = UserNotification()
    new_notification.userId = to_user; new_notification.notification = notification_data
    try:
        db.session.add(new_notification)
        db.session.commit()
        return True, new_notification, None
    except:
        db.session.rollback()
        return False, None, ADD_ENTRY_ERROR
    
def delete_notification(notification_ids_or_id: list[int] | int):
    if type(notification_ids_or_id) == list:
        row_deleted = db.session.query(UserNotification).filter(UserNotification.id.in_(notification_ids_or_id)).delete()
        db.session.commit()
        return True, row_deleted, None
    else:
        row_deleted = db.session.query(UserNotification).filter(UserNotification.id == notification_ids_or_id).delete()
        db.session.commit()
        return True, row_deleted, None

def search_user(user_id:int=None, name: str=None, email:str=None):
    query = db.session.query(User)
    if user_id != None:
        query = query.filter(User.id == user_id)
    if name != None:
        query = query.filter(User.name.like('%{}%'.format(name)))
    if email != None:
        query = query.filter(User.email.like('%{}%'.format(email)))
    
    result = query.all()
    return True, result, None

def change_user_role_and_restriction(user_id: int, new_role: str, isRestricted: bool = False):
    get_role_success, role, error = get_current_user_role()
    if check_user_authentication() == False and role != 'admin':
        return get_role_success, None, error
    
    current_user_id = current_user.id
    user = db.session.query(User).filter(User.id == user_id).first()
    if not user:
        return False, None, USER_NOT_EXIST
    if user.id == current_user_id:
        return False, None, CANNOT_CHANGE_SELF_ROLE
    
    user.role = new_role; user.isRestricted = isRestricted
    db.session.commit()
    return True, user, None

#Controller function of API to do data request 
def user_data_request(user_id:int=None):
    
    user = db.session.query(User).filter(User.id == user_id).all()
    user_info = db.session.query(UserInfo).filter(UserInfo.userId == user_id).all()
    user_session = db.session.query(Session).filter(Session.userId == user_id).all()
    user_borrow = db.session.query(BookBorrow).filter(BookBorrow.userId == user_id).all()
    user_favorite = db.session.query(BookFavorite).filter(BookFavorite.userId == user_id).all()
    user_notification = db.session.query(UserNotification).filter(UserNotification.userId == user_id).all()
    
    user_data = {}; user_data['user'] = user; user_data['user_info'] = user_info
    user_data['user_session'] = user_session; user_data['user_borrow'] = user_borrow
    user_data['user_favorite'] = user_favorite; user_data['user_notification'] = user_notification
    return True, user_data, None

def update_session_count(os_or_browser: str, type: str = 'browser'):
    
    updated_count = mysql_insert(MonthlySessionCount).values(browserOrOs=os_or_browser, type=type, count=1, lastUpdated=func.now())\
        .on_duplicate_key_update({
            'count': case(
                {(func.month(MonthlySessionCount.lastUpdated) != func.month(func.now())) | (func.year(MonthlySessionCount.lastUpdated) != func.year(func.now())): 1},
                else_=MonthlySessionCount.count + 1
            ),
            'lastUpdated': func.now()
        })
    db.session.execute(updated_count)
        

    # Check if update was successful (indicates no race condition)
    #if updated_count == 0:
    # Potential race condition, consider retrying or using a different approach
    #    print('No row update for monthly session count, potential race condition')
    db.session.commit()

def parse_user_agent(user_agent: str):
    parsed_user_agent = user_agent_parser.Parse(user_agent)
    browser_family = parsed_user_agent.get('user_agent').get('family')
    os_family = parsed_user_agent.get('os').get('family')
    return browser_family, os_family

def monthly_os_browser_count():
    data = db.session.query(MonthlySessionCount).all()
    return data

