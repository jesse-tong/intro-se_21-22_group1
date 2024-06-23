from flask import Blueprint, request
from global_vars.database_init import db
from sqlalchemy import func, distinct
import json, uuid
from flask_login import current_user
from flask_cors import CORS
from controller.library_controller import *
from global_vars.constants import status_template, result_per_page
from utils.get_status_object import get_status_object_json

#Blue print for miscellanous library settings
library_settings_routes = Blueprint('library_settings_routes', __name__)
CORS(library_settings_routes, supports_credentials=True, expose_headers=['X-CSRFToken'])

@library_settings_routes.route('/api/contacts', methods=['GET', 'POST'])
def contact_settings():
    if request.method == 'GET':
        contacts = get_library_contacts()
        if contacts == None:
            return get_status_object_json(False, None, DATABASE_ERROR), 500
        else:
            id, address, phone_number, email = contacts
            result = { 'address': address, 'phone_number': phone_number, 'email': email }
            return get_status_object_json(True, result, None), 200
    elif request.method == 'POST':
        address = request.form.get('address')
        phone_number = request.form.get('phone_number')
        email = request.form.get('email')
        success, error = update_library_contacts(address, phone_number, email)
        if success == True:
            contacts = get_library_contacts()
            id, address, phone_number, email = contacts
            result = { 'address': address, 'phone_number': phone_number, 'email': email }
            return get_status_object_json(True, result, None), 200
        else:
            return get_status_object_json(False, None, DATABASE_ERROR), 500
        
@library_settings_routes.route('/api/timings', methods=['GET', 'POST'])
def library_timings_settings():
    if request.method == 'GET':
        timings = get_library_timings()
        if timings == None:
            return get_status_object_json(False, None, DATABASE_ERROR), 500
        else:
            id, normal_open, normal_close, weekend_open, weekend_close, weekend_start, weekend_end = timings
            result = { 'normal_open': normal_open, 'normal_close': normal_close, 'weekend_open': weekend_open,
                      'weekend_close': weekend_close, 'weekend_start': weekend_start, 'weekend_end': weekend_end }
            return get_status_object_json(True, result, None), 200
    elif request.method == 'POST':
        normal_open = request.form.get('normal_open')
        normal_close = request.form.get('normal_close')
        weekend_open = request.form.get('weekend_open')
        weekend_close = request.form.get('weekend_close')
        weekend_start = request.form.get('weekend_start')
        weekend_end = request.form.get('weekend_end')

        try:
            weekend_start = int(weekend_start) if weekend_start != None else None
            weekend_end = int(weekend_end) if weekend_end != None else None
        except:
            return get_status_object_json(False, None, INVALID_PARAM), 400
        
        success, error = update_timings(normal_open, normal_close, weekend_open, weekend_close, weekend_start, weekend_end)

        if success == True:
            timings = get_library_timings()
            id, normal_open, normal_close, weekend_open, weekend_close, weekend_start, weekend_end = timings
            result = { 'normal_open': normal_open, 'normal_close': normal_close, 'weekend_open': weekend_open,
                      'weekend_close': weekend_close, 'weekend_start': weekend_start, 'weekend_end': weekend_end }
            return get_status_object_json(True, result, None), 200
        else:
            if error == INVALID_DURATION or error == INVALID_PARAM:
                return get_status_object_json(False, None, error), 400
            else:
                return get_status_object_json(False, None, error), 409