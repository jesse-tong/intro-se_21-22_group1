from werkzeug.security import generate_password_hash, check_password_hash
from models.user_model import User
from global_vars.database_init import db
import json
from global_vars.errors import *
from flask_login import login_user, login_required, current_user, logout_user

def register(email: str, password: str, name: str, role: str):
    user = User.query.filter_by(email = email).first()
    if (user):
        return False, None, EMAIL_EXISTS
    
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