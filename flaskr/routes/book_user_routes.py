from flask import Blueprint, url_for, request, make_response
from utils.get_status_object import get_status_object_json
from controller.book_controller import get_book_data
from controller.book_user_controller import *
from controller.user_controller import get_current_user_role
from models.book_model import Book
from models.user_book import BookFavorite, BookBorrow
import json, uuid, datetime
from dateutil.parser import parse as dateparse
from flask_login import current_user
from flask_cors import CORS

book_user = Blueprint('book_user', __name__)
CORS(book_user, supports_credentials=True, origins = r"https?:\/\/(?:w{1,3}\.)?[^\s.]+(?:\.[a-z]+)*(?::\d+)?(?![^<]*(?:<\/\w+>|\/?>))",
    expose_headers=['X-CSRFToken'])

@book_user.route('/api/borrow', methods=['GET', 'POST'])
def borrow_book_current_user():
    if request.method == 'GET':
        success, role, error = get_current_user_role()
        if not success:
            return get_status_object_json(False, None, NOT_AUTHENTICATED), 401
        else:
            user_id = current_user.id
            page = request.args.get('page')
            limit = request.args.get('limit')
            try:
                get_returned_book = request.args.get('get_returned')
                if get_returned_book == True or get_returned_book == '1' or str(get_returned_book).lower() == 'true':
                    get_returned_book == True
                else:
                    get_returned_book == False
                
            except:
                get_returned_book == False
            try:
                page = int(page) if page != None else None
                limit = int(limit) if limit != None else None
                if page != None and limit != None and (page <= 0 or limit <= 0):
                    raise ValueError()
            except:
                return get_status_object_json(False, None, INVALID_PARAM), 400
            success, result, error = search_borrow(user_id, page=page, limit=limit)
            if success == True:
                return get_status_object_json(True, result, error), 200
            else:
                return get_status_object_json(False, None, error), 200
    elif request.method== 'POST':
        if not current_user.is_authenticated:
            return get_status_object_json(False, None, NOT_AUTHENTICATED), 401
        else:
            user_id = current_user.id 
            book_id = request.form.get('book_id')
            if book_id == None:
                return get_status_object_json(False, None, INVALID_PARAM), 200
            else:
                try:
                    start_date = dateparse(request.form.get('start_borrow')) if request.form.get('start_borrow') != None else None
                except:
                    #Invalid start date, default current date (we don't need to use datetime.now(), the borrow_book() function already does it)
                    start_date = None
                try:
                    end_date = dateparse(request.form.get('end_borrow')) if request.form.get('end_borrow') != None else None
                except:
                    end_date = None

                success, result, error = borrow_book(user_id, book_id, start_date, end_date)
                return get_status_object_json(success, result, error), 200
    
@book_user.route('/api/borrow-search', methods=['GET', 'POST'])
def search_borrow_book_current_user():
    if not current_user.is_authenticated:
        return get_status_object_json(False, None, NOT_AUTHENTICATED), 401
    else:
        user_id = current_user.id 
        if request.method == 'GET':
            book_id = request.args.get('book_id')
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
        elif request.method == 'POST':
            book_id = request.form.get('book_id')
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')
        try:
            book_id = int(book_id)
            start_date = dateparse(start_date)
            end_date = dateparse(end_date)
        except:
            return get_status_object_json(False, None, INVALID_PARAM), 400
        
        success, result, error = search_borrow(user_id, book_id, start_date, end_date)
        return get_status_object_json(success, result, error), 200

@book_user.route('/api/get-borrow-fee', methods=['GET'])
def get_borrow_fee_route():
    borrow_id = request.args.get('borrow_id')
    additional_fees = request.args.get('additional_fees')
    try:
        borrow_id = int(borrow_id)
        additional_fees = float(additional_fees)
    except:
        return get_status_object_json(False, None, INVALID_PARAM), 400
    success, result, error = get_borrow_fee(borrow_id, additional_fees)
    return get_status_object_json(success, result, error)


@book_user.route('/api/manage-borrow-admin', methods=['GET', 'POST', 'PUT', 'DELETE'])
def admin_book_borrow_manage():
    success, role, error = get_current_user_role()
    if role != 'admin':
        return get_status_object_json(False, None, NOT_AUTHENTICATED), 401
    
    if request.method == 'GET':
        user_id = request.args.get('user_id')
        book_id = request.args.get('book_id')
        borrow_from = request.args.get('start_borrow') #find all loans that is after this date
        borrow_end = request.args.get('end_borrow')
        try:
            user_id = int(user_id)
            book_id = int(book_id)
            borrow_from = dateparse(borrow_from)
            borrow_end = dateparse(borrow_end)
        except:
            return get_status_object_json(False, None, INVALID_PARAM), 400
        success, search_result, error = search_borrow(user_id, book_id, borrow_from, borrow_end)

        return get_status_object_json(success, search_result, error), 200

    elif request.method == 'POST':

        book_id = request.form.get('book_id')
        user_id = request.form.get('user_id')
        start_borrow = request.form.get('start_borrow')
        end_borrow = request.form.get('end_borrow')
        return_date = request.form.get('return_date')

        try:
            book_id = int(book_id)
            user_id = int(user_id)
            start_borrow = dateparse(start_borrow) if start_borrow != None else None
            end_borrow = dateparse(end_borrow) if end_borrow != None else None
            return_date = dateparse(return_date) if return_date != None else None
        except:
            return get_status_object_json(False, None, INVALID_PARAM), 400
        
        success, result, error = borrow_book(user_id, book_id, start_borrow, end_borrow)
        return get_status_object_json(success, result, error), 200
    elif request.method == 'PUT':
        borrow_id = request.form.get('borrow_id')
        book_id = request.form.get('book_id')
        user_id = request.form.get('user_id')
        start_borrow = request.form.get('start_borrow')
        end_borrow = request.form.get('end_borrow')
        return_date = request.form.get('return_date')
        has_returned = True if return_date != None else False
        damaged_or_lost = request.form.get('damaged_or_lost')

        if damaged_or_lost == None or damaged_or_lost.lower() == 'false' or damaged_or_lost == '0':
            damaged_or_lost = False
        elif damaged_or_lost.lower() == 'true' or damaged_or_lost == '1':
            damaged_or_lost = True
        else:
            return get_status_object_json(False, None, INVALID_PARAM)

        try:
            borrow_id = int(borrow_id)
            book_id = int(book_id) if book_id != None else None
            user_id = int(user_id) if user_id != None else None
            start_borrow = dateparse(start_borrow) if start_borrow != None else None
            end_borrow = dateparse(end_borrow) if end_borrow != None else None
            return_date = dateparse(return_date) if return_date != None else None
        except:
            return get_status_object_json(False, None, INVALID_PARAM), 400
        
        success, result, error = edit_borrow(borrow_id, user_id, book_id, start_borrow, end_borrow, has_returned, return_date, damaged_or_lost)
        return get_status_object_json(success, result, error), 200
    elif request.method == 'DELETE':
        borrow_id = request.form.get('borrow_id')
        success, result, error = delete_borrow(borrow_id)

        return get_status_object_json(success, result, error)

@book_user.route('/api/return/<borrow_id>', methods=['POST', 'GET'])
def return_book_current_user(borrow_id):
    if not current_user.is_authenticated:
        return get_status_object_json(False, None, NOT_AUTHENTICATED), 401
    else:
        try:
            user_id = current_user.id
        except:
            return get_status_object_json(False, None, INVALID_PARAM), 400

        success, result, error = return_book(user_id,  borrow_id)
        return get_status_object_json(success, result, error), 200

