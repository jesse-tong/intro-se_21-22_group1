import os
from flask import Blueprint, request, make_response, jsonify, send_file
from global_vars.database_init import db
from models.user_model import User, UserInfo
from flask_login import logout_user, current_user
from utils.file_utils import save_user_image, delete_user_image, delete_user_image_dir, get_save_user_image_path
from utils.get_status_object import get_status_object_json
from flask_cors import CORS
from flask_wtf.csrf import generate_csrf
from controller.user_controller import login, register, isRestricted, change_password, add_update_user_infos, user_profile, search_user
from global_vars.constants import *
from global_vars.errors import *
from dataclasses import asdict

auth = Blueprint('auth', __name__)

#Since we send CSRF token from the headers, we need to expose it through CORS 
# or the browser and frontend would not get
CORS(auth, supports_credentials=True, origins = r"https?:\/\/(?:w{1,3}\.)?[^\s.]+(?:\.[a-z]+)*(?::\d+)?(?![^<]*(?:<\/\w+>|\/?>))", expose_headers=['X-CSRFToken'])

#This is used to generate csrf token when the client requests this
@auth.route('/auth/csrf_token', methods=['GET', 'HEAD'])
def set_xsrf_cookie():
    response = make_response('')
    csrf_token = generate_csrf()
    response.set_cookie('X-CSRFToken', csrf_token)
    response.headers.add('X-CSRFToken', csrf_token)
    return response

@auth.route('/auth/login', methods=['POST'])
def login_route():
    login_data = request.form
    email = login_data.get('email')
    password = login_data.get('password')
    remember = True if login_data.get('remember') != None else False

    result, user_obj, error = login(email, password, remember)
    if result == True:

        return get_status_object_json(result, user_obj, error), 200
    else:
        return get_status_object_json(result, user_obj, error), 401

@auth.route('/auth/logout', methods=['GET', 'POST'])
def logout_route():
    logout_user()
    return get_status_object_json(True, None, None), 200

@auth.route('/auth/register', methods=['POST'])
def register_route():
    register_form = request.form
    email = register_form.get('email')
    password = register_form.get('password')
    name = register_form.get('name')
    role = register_form.get('role')
    result, user, error = register(email, password, name, role)
    return get_status_object_json(result, user, error), 200

@auth.route('/auth/change-password', methods=['POST'])
def change_password_route():
    form = request.form
    result, user, error = change_password(form.get('old_password'), form.get('new_password'))
    return get_status_object_json(result, user, error), 200

@auth.route('/auth/is-restricted/<userId>')
def is_user_restricted(userId):
    try:
        id = int(userId)
        result = isRestricted(id)
        return get_status_object_json(True, result, None), 200
    except:
        return get_status_object_json(False, None, INVALID_ID), 400
    
@auth.route('/auth/update-user-info', methods=['POST', 'PUT'])
def update_user_info():
    if not current_user.is_authenticated:
        return get_status_object_json(False, None, NOT_AUTHENTICATED), 403
    else:
        user_id = current_user.id 
        age = request.form.get('age')
        gender = request.form.get('gender')
        phone_number = request.form.get('phone_number')
        address = request.form.get('address')

        if gender != None and gender.lower() not in available_genders:
            return get_status_object_json(False, None, INVALID_PARAM), 400
        
        try:
            age = int(age) if age != None else None
        except:
            return get_status_object_json(False, None, INVALID_PARAM), 400
        
        if age != None and (age < 0 or age > 125): 
            return get_status_object_json(False, None, INVALID_PARAM), 400
        
        success, result, error = add_update_user_infos(user_id, age, gender, borrow_left_default, phone_number, address)
        return get_status_object_json(success, result, error), 200

@auth.route('/auth/profile', methods=['GET'])
def profile_route():
    if not current_user.is_authenticated:
        return get_status_object_json(False, None, NOT_AUTHENTICATED), 403
    else:
        success, result, error = user_profile(current_user.id)
        if result != None:
            result = asdict(result[0]) | asdict(result[1])
        return get_status_object_json(success, result, error), 200
    
@auth.route('/auth/profile/<user_id>', methods=['GET'])
def profile_route_with_id(user_id):
    try:
        user_id = int(user_id)
        success, result, error = user_profile(user_id)
        if result != None:
            result = asdict(result[0]) | asdict(result[1])
        return get_status_object_json(success, result, error), 200
    except:
        return get_status_object_json(False, None, USER_NOT_EXIST), 404
    
@auth.route('/api/search-user', methods=['GET'])
def search_user_route():
    user_id = request.args.get('user_id')
    name = request.args.get('name')
    email = request.args.get('email')
    
    try:
        user_id = int(user_id) if user_id != None else None
    except:
        return get_status_object_json(False, None, INVALID_PARAM), 400

    success, result, error = search_user(user_id, name, email)
    return get_status_object_json(success, result, error)

@auth.route('/api/profile_image/<user_id>', methods=['GET', 'POST', 'DELETE'])
def profile_image_routes(user_id):
    if request.method == 'GET':
        try:
            user_id = int(user_id)
        except:
            return get_status_object_json(False, None, INVALID_PARAM), 404
        user = db.session.query(User).filter(User.id == user_id).first()
        if not user:
            return get_status_object_json(False, None, INVALID_ID), 404
        
        saved_user_image_path = db.session.query(UserInfo).filter(UserInfo.userId == user_id).first()

        if saved_user_image_path == None or saved_user_image_path.imagePath == None:
            return get_status_object_json(False, None, NO_FILE_UPLOADED), 404
        user_image_name = saved_user_image_path.imagePath

        user_image_path = get_save_user_image_path(user_id, user_image_name)

        if os.path.isfile(user_image_path):
            return send_file(user_image_path, as_attachment=False), 200
        else:
            return get_status_object_json(False, None, NO_FILE_UPLOADED), 404
    elif request.method == 'POST':
        try:
            user_id = int(user_id)
        except:
            return get_status_object_json(False, None, INVALID_PARAM), 400
        user = db.session.query(User).filter(User.id == user_id).first()

        if not user:
            return get_status_object_json(False, None, INVALID_ID), 400
        file = request.files.get('user_image')
        if not file:
            return get_status_object_json(False, None, NO_FILE_UPLOADED), 400
        user_image_name = file.filename
        try:
            user_image_extension = file.mimetype.split('/')[0]
            if user_image_extension != 'image':
                return get_status_object_json(False, None, INVALID_FILE)
        except:
            return get_status_object_json(False, None, INVALID_FILE)
        
        image_bytes = file.read()
        save_user_image(image_bytes, user_id, user_image_name)
        saved_user_info = db.session.query(UserInfo).filter(UserInfo.userId == user_id).first()

        if saved_user_info != None and saved_user_info.imagePath != None:
            delete_user_image(user_id, saved_user_info.imagePath)
        
        if saved_user_info == None:
            create_new = True
            saved_user_info = UserInfo()
            saved_user_info.userId == user_id
        else:
            create_new = False
        
        if create_new == True:
            db.session.add(saved_user_info)
        saved_user_info.imagePath = user_image_name
        db.session.commit()

        return get_status_object_json(True, True, None)
    elif request.method == 'DELETE':
        try:
            user_id = int(user_id)
        except:
            return get_status_object_json(False, None, INVALID_PARAM), 400
        user = db.session.query(User).filter(User.id == user_id).first()
        if not user:
            return get_status_object_json(False, None, INVALID_ID), 400

        try:
            saved_user_info = db.session.query(UserInfo).filter(UserInfo.userId == user_id).first()
            if saved_user_info != None and saved_user_info.imagePath != None:
                delete_user_image(user_id, saved_user_info.imagePath)
                delete_user_image_dir(user_id)

            db.session.query(UserInfo).filter(UserInfo.userId == user_id).delete()
            db.session.commit()
            return get_status_object_json(True, None, None), 200
        except:
            return get_status_object_json(False, None, DELETE_ERROR), 409
