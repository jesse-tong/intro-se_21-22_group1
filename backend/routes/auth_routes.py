from flask import Blueprint, request, make_response, jsonify
from global_vars.database_init import db
from flask_login import logout_user
import json
from utils.get_status_object import get_status_object_json
from flask_cors import CORS
from flask_wtf.csrf import generate_csrf
from controller.user_controller import login, register, isRestricted, change_password
from global_vars.errors import *

auth = Blueprint('auth', __name__)

#Since we send CSRF token from the headers, we need to expose it through CORS 
# or the browser and frontend would not get
CORS(auth, supports_credentials=True, origins = r"https?:\/\/(?:w{1,3}\.)?[^\s.]+(?:\.[a-z]+)*(?::\d+)?(?![^<]*(?:<\/\w+>|\/?>))",
    expose_headers=['X-CSRFToken'])

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
    

