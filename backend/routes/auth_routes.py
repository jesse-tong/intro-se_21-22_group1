import os
from datetime import timedelta
from flask import Blueprint, request, make_response, jsonify, send_file, url_for, redirect, flash
from flask_login import login_user
from global_vars.database_init import db
from models.user_model import User, UserInfo, Session
from models.library_misc import ArticleImage, Article
from flask_login import logout_user, current_user
from utils.file_utils import save_user_image, delete_user_image, get_save_user_image_path
from utils.get_status_object import get_status_object_json
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from flask_wtf.csrf import generate_csrf
from controller.user_controller import *
from global_vars.constants import *
from global_vars.errors import *
from dataclasses import asdict
from authlib.integrations.flask_client import OAuth
from urllib import parse as url_parse
from utils.time_utils import ip_address_to_country


auth = Blueprint('auth', __name__)
oauth_client = OAuth()
server_domain = os.environ.get('VITE_API_POINT')
server_scheme = url_parse.urlparse(server_domain).scheme
csrf = CSRFProtect()

#Since we send CSRF token from the headers, we need to expose it through CORS 
# or the browser and frontend would not get
CORS(auth, supports_credentials=True, origins = r"https?:\/\/(?:w{1,3}\.)?[^\s.]+(?:\.[a-z]+)*(?::\d+)?(?![^<]*(?:<\/\w+>|\/?>))", expose_headers=['X-CSRFToken'])

#This is used to generate csrf token when the client requests this

@auth.route('/auth/csrf_token', methods=['GET', 'HEAD'])
@csrf.exempt
def set_xsrf_cookie():
    csrf_token = generate_csrf()
    response = make_response(jsonify({'csrf_token': csrf_token}))
    response.set_cookie('X-CSRFToken', csrf_token)
    response.headers.add('X-CSRFToken', csrf_token)
    return response

@auth.route('/analytics', methods=['GET', 'POST'])
def analytics():
    
    user_agent = request.user_agent.string
    browser, os_family = parse_user_agent(user_agent)
    update_session_count(browser, 'browser')
    update_session_count(os_family, 'os')
    #ip_address = request.remote_addr
    if request.environ.get('HTTP_CF_CONNECTING_IP') != None:
        ip_address = request.environ['HTTP_CF_CONNECTING_IP'] #Case of running behind Cloudflare's tunnel
    elif request.environ.get('HTTP_X_FORWARDED_FOR') != None:
        ip_address = request.environ['HTTP_X_FORWARDED_FOR'] #Case of running behind reverse proxy server of Apache/Nginx
    else:
        ip_address = request.environ['REMOTE_ADDR']
    country_codes_and_name = ip_address_to_country(ip_address)
    
    if country_codes_and_name != None:
        #Store ISO 3166 numeric code since it's more consistent than country codes or names
        country_iso_numeric = country_codes_and_name[1] 
        update_session_count(country_iso_numeric, 'country')
        
    if request.environ.get('HTTP_REFERER') != None:
        referer = request.environ['HTTP_REFERER'] #Case of running befind reverse proxy or tunnel
    elif request.environ.get('HTTP_REFERER') == None and request.method == 'POST':
        referer = request.form.get('referer')
    else:
        referer = request.args.get('referer')
    
    if check_user_authentication():
        user = db.session.query(User).filter(User.id == current_user.id).first()
        if user != None:
            session = db.session.query(Session).filter(Session.browser == browser).filter(Session.os == os_family) \
                .filter(Session.ipAddress == ip_address).filter(Session.userId == user.id).first()
            if not session:
                #If the user has logged in, and detect logged in new browser/os/IP address, note it
                new_session = Session(userId=user.id, os=os_family, browser=browser, referer=referer, ipAddress=ip_address)
                try:
                    db.session.add(new_session); db.session.commit()
                except:
                    pass

    return request.user_agent.string

@auth.route('/auth/sessions', methods=['GET'])
def get_user_session():
    if not check_user_authentication():
        return get_status_object_json(False, None, NOT_AUTHENTICATED), 403
    
    current_user_id = current_user.id
    sessions = db.session.query(Session).filter(Session.userId == current_user_id).all()
    return get_status_object_json(True, sessions, None), 200

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

@auth.route('/auth/send-verification-email/<user_id>', methods=['GET', 'POST'])
async def send_verification_email_route(user_id):
    try:
        user_id = int(user_id)
    except:
        return get_status_object_json(False, None, INVALID_ID), 400
    
    user = db.session.query(User).filter(User.id == user_id).first()
    if not user:
        return get_status_object_json(False, None, INVALID_ID), 404
    
    success, result, error = await send_verification_email_controller(user_id)
    return get_status_object_json(success, result, error), 200

@auth.route('/auth/register', methods=['POST'])
async def register_route():
    register_form = request.form
    email = register_form.get('email')
    password = register_form.get('password')
    name = register_form.get('name')
    role = register_form.get('role')
    resend_verification_email = register_form.get('resend_verification')
    if resend_verification_email == 'true' or resend_verification_email == '1':
        resend_verification_email = True
    else:
        resend_verification_email = False
    result, user, error = await register(email, password, name, role, resend_verification_email)
    return get_status_object_json(result, user, error), 200

@auth.route('/auth/verification/<token>')
def verify_email_address_route(token, methods=['POST', 'GET']):
    success, result, error = verify_email_address(token)
    return redirect('/login?verify_success=' + ('true' if success == True else 'false') + ('&error=' + error if error != None else '' ))

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

@auth.route('/auth/update-library-card-info', methods=['POST', 'PUT'])
def update_library_card_info_route():
    if not check_user_authentication():
        return get_status_object_json(False, None, NOT_AUTHENTICATED), 403
    else:
        user_id = current_user.id 
        age = request.form.get('age')
        gender = request.form.get('gender')
        phone_number = request.form.get('phone_number')
        address = request.form.get('address')
        alternate_email = request.form.get('alternate_email')
        alternate_phone = request.form.get('alternate_phone')
        zip_code = request.form.get('zip_code')

        if gender != None and gender.lower() not in available_genders:
            return get_status_object_json(False, None, INVALID_PARAM), 400
        
        try:
            age = int(age) if age != None else None
        except:
            return get_status_object_json(False, None, INVALID_PARAM), 400
        
        if age != None and (age < 0 or age > 125): 
            return get_status_object_json(False, None, INVALID_PARAM), 400
        
        success, result, error = add_update_library_card_infos(user_id, age, gender, borrow_left_default, 
                                                       phone_number, address, alternate_email, alternate_phone, zip_code)
        return get_status_object_json(success, result, error), 200

@auth.route('/auth/update-user-info', methods=['POST', 'PUT'])
def update_user_info():
    if not check_user_authentication():
        return get_status_object_json(False, None, NOT_AUTHENTICATED), 403
    else:
        user_id = current_user.id 
        age = request.form.get('age')
        gender = request.form.get('gender')
        phone_number = request.form.get('phone_number')
        address = request.form.get('address')
        alternate_email = request.form.get('alternate_email')
        alternate_phone = request.form.get('alternate_phone')
        zip_code = request.form.get('zip_code')

        if gender != None and gender.lower() not in available_genders:
            return get_status_object_json(False, None, INVALID_PARAM), 400
        
        try:
            age = int(age) if age != None else None
        except:
            return get_status_object_json(False, None, INVALID_PARAM), 400
        
        if age != None and (age < 0 or age > 125): 
            return get_status_object_json(False, None, INVALID_PARAM), 400
        
        success, result, error = add_update_user_infos(user_id, age, gender, borrow_left_default, 
                                                       phone_number, address, alternate_email, alternate_phone, zip_code)
        return get_status_object_json(success, result, error), 200

@auth.route('/auth/profile', methods=['GET'])
def profile_route():
    if not check_user_authentication():
        return get_status_object_json(False, None, NOT_AUTHENTICATED), 403
    else:
        success, result, error = user_profile(current_user.id)
        if result != None:
            result = asdict(result[0]) | asdict(result[1]) if result[1] != None else result[0]
        return get_status_object_json(success, result, error), 200

@auth.route('/auth/profile/<user_id>', methods=['GET'])
def profile_route_with_id(user_id):
    try:
        user_id = int(user_id)
        success, result, error = user_profile(user_id)
        if result != None:
            result = asdict(result[0]) | asdict(result[1]) if result[1] != None else result[0]
        return get_status_object_json(success, result, error), 200
    except:
        return get_status_object_json(False, None, USER_NOT_EXIST), 404

@auth.route('/auth/library_card', methods=['GET'])
def get_logged_in_user_library_card(user_id):
    if not check_user_authentication():
        return get_status_object_json(False, None, NOT_AUTHENTICATED), 403
    
    try:
        user_id = int(user_id)
        success, result, error = library_card_of_user(current_user.id)
        if result != None:
            if result[1] == None:
                return get_status_object_json(False, None, LIBRARY_CARD_NOT_EXIST), 404
            result = asdict(result[0]) | asdict(result[1])
        return get_status_object_json(success, result, error), 200
    except:
        return get_status_object_json(False, None, USER_NOT_EXIST), 404

@auth.route('/auth/library_card/<user_id>', methods=['GET'])
def get_library_card_with_id(user_id):
    _, role, __ = get_current_user_role()
    if not check_user_authentication():
        return get_status_object_json(False, None, NOT_AUTHENTICATED), 403
    if role != 'admin' or current_user.id != user_id:
        return get_status_object_json(False, None, INVALID_AUTH), 403
    
    try:
        user_id = int(user_id)
        success, result, error = library_card_of_user(user_id)
        if result != None:
            result = asdict(result[0]) | asdict(result[1]) if result[1] != None else result[0]
        return get_status_object_json(success, result, error), 200
    except:
        return get_status_object_json(False, None, USER_NOT_EXIST), 404
    
@auth.route('/api/search-user', methods=['GET'])
def search_user_route():
    user_id = request.args.get('user_id')
    name = request.args.get('name')
    email = request.args.get('email')
    page = request.args.get('page')
    limit = request.args.get('limit')

    try:
        user_id = int(user_id) if user_id != None else None
        page = int(page) if page != None else None
        limit = int(limit) if limit != None else None
    except:
        return get_status_object_json(False, None, INVALID_PARAM), 400
    
    if page != None and limit != None and page <= 0 or limit <= 0:
        return get_status_object_json(False, None, INVALID_PARAM), 409

    success, result, error = search_user(user_id, name, email, page, limit)
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
    
    if not check_user_authentication() or current_user.id != user_id:
        return get_status_object_json(False, None, INVALID_AUTH), 403

    success, data, error = user_data_request(user_id)
    return get_status_object_json(success, data, error), 200

@auth.route('/login/google')
def login_google():
    redirect_uri = url_for('auth.google_auth', _scheme=server_scheme, _external=True)
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
        if not check_user_authentication():
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
        if not check_user_authentication():
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
        if not check_user_authentication():
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

@auth.route('/api/monthly-session-data')
def monthly_session_data_route():
    data = monthly_os_browser_count()
    return get_status_object_json(True, data, None), 200

@auth.route('/api/get-users')
def get_users_route():
    page = request.args.get('page')
    limit = request.args.get('limit')
    try:
        page = int(page) if page != None else None
        limit = int(limit) if limit != None else None
    except:
        return get_status_object_json(False, None, INVALID_PARAM), 400
    if page <= 0 or limit <= 0: 
        return get_status_object_json(False, None, INVALID_PARAM), 409
    if page != None and limit != None: 
        users = db.session.query(User).offset((page - 1)*limit).limit(limit).all()
    else:
        users = db.session.query(User).all()
    return get_status_object_json(True, users, None), 200

@auth.route('/api/change-user-role-and-restriction', methods=['POST'])
def change_user_role_and_restriction_route():
    success, role, error = get_current_user_role()
    if not check_user_authentication() and role != 'admin':
        return get_status_object_json(False, None, NOT_AUTHENTICATED), 403
    form = request.form
    user_id = form.get('user_id')
    role = form.get('role')
    isRestricted = form.get('is_restricted')
    try:
        user_id = int(user_id)
        isRestricted = True if isRestricted == 'true' or isRestricted == '1' else False
    except:
        return get_status_object_json(False, None, INVALID_PARAM), 400
    success, result, error = change_user_role_and_restriction(user_id, role, isRestricted)
    return get_status_object_json(success, result, error), 200