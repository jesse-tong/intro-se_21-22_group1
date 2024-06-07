from werkzeug.security import generate_password_hash, check_password_hash
from models.user_model import User, UserInfo, UserNotification
from global_vars.database_init import db
import re
from global_vars.errors import *
from flask_login import login_user, login_required, current_user, logout_user

def register(email: str, password: str, name: str, role: str):
    user = User.query.filter_by(email = email).first()
    if (user):
        return False, None, EMAIL_EXISTS
    
    #Reference: https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    if re.fullmatch(email_regex, email) == None:
        return False, None, INVALID_EMAIL

    new_user = User(email = email, name = name, role = role, password = generate_password_hash(password=password))
    try:
        db.session.add(new_user)
        db.session.commit()

        return True, new_user, None
    except:
        db.session.rollback()
        return False, None, ADD_ENTRY_ERROR

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
    if not current_user.is_authenticated:
        return False, None, NOT_AUTHENTICATED
    
    user = db.session.query(User).filter(User.id == current_user.id).first()
    if not user or not (check_password_hash(user.password, old_password)):
        return False, None, INVALID_AUTH
    else:
        new_password_hash = generate_password_hash(new_password)
        user.password = new_password_hash
        db.session.commit()
        logout_user()
        return True, user, None

def get_current_user_role():
    if not current_user.is_authenticated:
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
    profile = db.session.query(User, UserInfo).join(UserInfo, User.id == UserInfo.userId).filter(User.id == user_id).first()
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
