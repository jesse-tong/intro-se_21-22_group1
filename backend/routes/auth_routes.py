import os
from datetime import timedelta
from flask import Blueprint, request, make_response, jsonify, send_file, url_for, redirect, flash
from flask_login import login_user
from global_vars.database_init import db
from models.user_model import User, UserInfo
from models.library_misc import ArticleImage, Article
from flask_login import logout_user, current_user
from utils.file_utils import save_user_image, delete_user_image, get_save_user_image_path
from utils.get_status_object import get_status_object_json
from flask_cors import CORS
from flask_wtf.csrf import generate_csrf
from controller.user_controller import login, register, isRestricted, change_password, add_update_user_infos, user_profile, search_user, user_data_request
from global_vars.constants import *
from global_vars.errors import *
from dataclasses import asdict
from authlib.integrations.flask_client import OAuth

auth = Blueprint('auth', __name__)
oauth_client = OAuth()

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
                

            db.session.query(UserInfo).filter(UserInfo.userId == user_id).delete()
            db.session.commit()
            return get_status_object_json(True, None, None), 200
        except:
            return get_status_object_json(False, None, DELETE_ERROR), 409
        
@auth.route('/data-request/<user_id>', methods=['GET'])
def data_request_route(user_id):
    try:
        user_id = int(user_id)
    except:
        return get_status_object_json(False, None, INVALID_ID), 400
    
    user = db.session.query(User).filter(User.id == user_id).first()
    if not user:
        return get_status_object_json(False, None, INVALID_ID), 409
    
    if not current_user.is_authenticated or current_user.id != user_id:
        return get_status_object_json(False, None, INVALID_AUTH), 403

    success, data, error = user_data_request(user_id)
    return get_status_object_json(success, data, error), 200

@auth.route('/login/google')
def login_google():
    redirect_uri = url_for('auth.google_auth', _external=True)
    return oauth_client.google.authorize_redirect(redirect_uri)
    
@auth.route('/auth/google')
def google_auth():
    token = oauth_client.google.authorize_access_token()
    profile = oauth_client.google.userinfo(token=token)
    email = profile.get('email')
    name = profile.get('name')
    user = db.session.query(User).filter(User.email == email).first()
    if not user:
        user = User(); user.email = email; user.name = name; user.role = 'user'
        db.session.add(user)
        try:
            db.session.commit()
        except:
            return redirect('/login?error={}'.format(GOOGLE_LOGIN_ERROR))
    
    session_duration = int(token.get('expires_in')) if token.get('expires_in') != None else 3600
    session_duration = timedelta(seconds=session_duration)
    result = login_user(user, remember=True, duration=session_duration)
    if result == True:
        return redirect('/?userId={}&name={}&role={}'.format(user.id, user.name, user.role))
    else:
        return redirect('/login?error={}'.format(GOOGLE_LOGIN_ERROR))

@auth.route('/api/upload-user-image', methods=['GET', 'POST'])
def upload_image_user():
    if request.method == 'GET':
        if not current_user.is_authenticated:
            return get_status_object_json(False, None, NOT_AUTHENTICATED), 403
        #This one to get user's current uploaded image
        page = request.args.get('page')
        limit = request.args.get('limit')
        try:
            user_id = int(current_user.id)
            page = int(page) if page != None else None
            limit = int(limit) if limit != None else None
        except:
            return get_status_object_json(False, None, INVALID_PARAM), 400
        if page <= 0 or limit <= 0:
            return get_status_object_json(False, None, INVALID_PARAM), 409
        if page != None and limit != None:
            offset = (page - 1)*limit
            images_details = db.session.query(ArticleImage).filter(ArticleImage.userId == user_id).offset(offset).limit(limit).all()
        else:
            images_details = db.session.query(ArticleImage).filter(ArticleImage.userId == user_id).all()

        return get_status_object_json(True, images_details, None), 200
    elif request.method == 'POST':
        if not current_user.is_authenticated:
            return get_status_object_json(False, None, NOT_AUTHENTICATED), 403
        try:
            user_id = int(current_user.id)
        except:
            return get_status_object_json(False, None, INVALID_PARAM), 400
        user = db.session.query(User).filter(User.id == user_id).first()

        if not user:
            return get_status_object_json(False, None, INVALID_ID), 400
        file = request.files.get('file')
        if not file:
            return get_status_object_json(False, None, NO_FILE_UPLOADED), 400
        image_filename = file.filename
        try:
            image_extension = file.mimetype.split('/')[0]
            if image_extension != 'image':
                return get_status_object_json(False, None, INVALID_FILE)
        except:
            return get_status_object_json(False, None, INVALID_FILE)
        
        image_bytes = file.read()
        save_user_image(image_bytes, user_id, image_filename)
        
        saved_image_data = ArticleImage()
        saved_image_data.userId = user_id
        saved_image_data.imagePath = image_filename
        db.session.add(saved_image_data)
        
        db.session.commit()

        return get_status_object_json(True, saved_image_data, None)

@auth.route('/api/upload-user-image/<image_id>', methods=['DELETE'])
def delete_upload_user_image_route(image_id):
    if request.method == 'DELETE':
        if not current_user.is_authenticated:
            return get_status_object_json(False, None, NOT_AUTHENTICATED), 403
        try:
            user_id = int(current_user.id)
            image_id = int(image_id)
        except:
            return get_status_object_json(False, None, INVALID_PARAM), 400
        user = db.session.query(User).filter(User.id == user_id).first()

        if not user:
            return get_status_object_json(False, None, INVALID_ID), 400

        try:
            saved_image_data = db.session.query(ArticleImage).filter(ArticleImage.id == image_id).filter(ArticleImage.userId == user_id).first()
            if saved_image_data != None and saved_image_data.imagePath != None:
                #Check if there are other records that share the same image name, if none delete it
                shared_image_records = db.session.query(ArticleImage).filter(ArticleImage.imagePath == saved_image_data.imagePath) \
                                        .filter(ArticleImage.id != saved_image_data.id).all()
                if len(shared_image_records) == 0:
                    delete_user_image(user_id, saved_image_data.imagePath)

            db.session.query(ArticleImage).filter(ArticleImage.id == image_id).filter(ArticleImage.userId == user_id).delete()
            db.session.commit()
            return get_status_object_json(True, None, None), 200
        except:
            return get_status_object_json(False, None, DELETE_ERROR), 409
        
@auth.route('/uploaded-image/<image_id>', methods=['GET'])
def get_uploaded_image(image_id):
    if request.method == 'GET':
        try:
            image_id = int(image_id)
        except:
            return get_status_object_json(False, None, INVALID_PARAM), 404
        image = db.session.query(ArticleImage).filter(ArticleImage.id == image_id).first()
        if not image:
            return get_status_object_json(False, None, INVALID_ID), 404
        
        saved_image_file_path = db.session.query(ArticleImage).filter(ArticleImage.id == image_id).first()

        if saved_image_file_path == None:
            return get_status_object_json(False, None, NO_FILE_UPLOADED), 404
        image_file_name = saved_image_file_path.imagePath

        image_path = get_save_user_image_path(saved_image_file_path.userId, image_file_name)

        if os.path.isfile(image_path):
            return send_file(image_path, as_attachment=False), 200
        else:
            return get_status_object_json(False, None, NO_FILE_UPLOADED), 404