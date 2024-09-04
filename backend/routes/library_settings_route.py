from flask import Blueprint, request, jsonify, render_template_string, redirect
import requests
from requests.auth import HTTPBasicAuth
from global_vars.database_init import db
from sqlalchemy import func, distinct
import json, uuid, stripe
from flask_login import current_user
from flask_cors import CORS
from controller.library_controller import *
from controller.user_controller import check_user_authentication
from controller.book_user_controller import get_borrow_fee, set_borrow_resolve, delete_borrow
from models.user_book import BookBorrow
from global_vars.constants import status_template, result_per_page
from utils.get_status_object import get_status_object_json
from utils.file_utils import *
import datetime
from models.user_model import User
from dateutil.parser import parse as dateparse
from controller.book_user_controller import get_policies

#Blue print for miscellanous library settings
library_settings_routes = Blueprint('library_settings_routes', __name__)
CORS(library_settings_routes, supports_credentials=True, origins = r"https?:\/\/(?:w{1,3}\.)?[^\s.]+(?:\.[a-z]+)*(?::\d+)?(?![^<]*(?:<\/\w+>|\/?>))", expose_headers=['X-CSRFToken'])

stripe_publishable_key = os.environ.get('STRIPE_PUBLISHABLE_KEY')
stripe_secret_key = os.environ.get('STRIPE_SECRET_KEY')
server_domain = os.environ.get('VITE_API_POINT')
paypal_client_id = os.environ.get('PAYPAL_CLIENT_ID')
paypal_client_secret = os.environ.get('PAYPAL_CLIENT_SECRET')

def convert_to_stripe(amount: float, currency: str):
    #Since Stripe requires charged amount of cents or equilvalent (for example, 10 USD becomes 1000)
    zero_decimal_currencies = ['bif', 'clp', 'jpy', 'kmf', 'mga', 'pyg', 'rwf', 'vnd', 'xaf', 'xof']
    #Currencies which Stripe requires the last digit is zero
    three_decimal_currencies = ['bhd', 'jod', 'kwd', 'omr', 'tnd']
    #Currencies which recently switched to zero decimal, for compatibility reasons the last two digits must be zeros
    zero_decimal_compat = ['isk', 'huf', 'twd', 'ugx']
    if currency in zero_decimal_currencies:
        return int(amount)
    elif currency in three_decimal_currencies:
        return int(round(amount*1000, -1))
    elif currency  in zero_decimal_compat:
        return int(round(amount*100, -2))
    else:
        return int(amount*100)

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
            
@library_settings_routes.route('/api/article/<article_id>', methods=['GET', 'PUT', 'DELETE'])
def get_put_delete_article_route(article_id):
    try:
        article_id = int(article_id)
    except:
        return get_status_object_json(False, None, INVALID_ID), 400
    if request.method == 'GET':
        success, article, error = get_article(article_id)
        return get_status_object_json(success, article, error), 200
    elif request.method == 'PUT':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category')
        note = request.form.get('note')
        thumbnail = request.form.get('thumbnail')
        success, edited_article, error = edit_article(article_id, title, content, category, note, thumbnail)
        return get_status_object_json(success, edited_article, error), 200
    elif request.method == 'DELETE':
        success, result, error = delete_article(article_id)
        return get_status_object_json(success, result, error), 200

@library_settings_routes.route('/api/article', methods=['GET', 'POST'])
def get_post_articles_route():
    if request.method == 'GET':
        try:
            page = int(request.args.get('page')) if request.args.get('page') != None else None
            limit = int(request.args.get('limit')) if request.args.get('limit') != None else None
        except:
            return get_status_object_json(False, None, INVALID_PARAM), 400
        
        success, article_summaries, error = get_article_summaries(page, limit, True)
        return get_status_object_json(success, article_summaries, error)
    elif request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category')
        note = request.form.get('note')
        thumbnail = request.form.get('thumbnail')
        success, added_article, error = add_article(title, content, category, note, thumbnail)
        return get_status_object_json(success, added_article, error), 200
    
@library_settings_routes.route('/get-stripe-key')
def get_stripe_publishable_key():
    stripe_config = {"publicKey": stripe_publishable_key}
    return jsonify(stripe_config)

@library_settings_routes.route('/get-paypal-key')
def get_paypal_client_id():
    paypal_config = {"publicKey": paypal_client_id}
    return jsonify(paypal_config)

@library_settings_routes.route("/create-checkout-session-paypal/<borrow_id>/<order_id>", methods=['GET', 'POST'])
def create_checkout_session_paypal(borrow_id, order_id):
    if not check_user_authentication():
        return get_status_object_json(False, None, NOT_AUTHENTICATED), 403
    
    try:
        borrow_id = int(borrow_id)
    except:
        return get_status_object_json(False, None, INVALID_ID), 409
    
    borrow = db.session.query(BookBorrow).filter(BookBorrow.id == borrow_id).filter(BookBorrow.userId == current_user.id).first()
    if not borrow:
        return get_status_object_json(False, None, NOT_AUTHENTICATED), 403
    
    
    
    api_link = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}/capture"    
    client_id = paypal_client_id   
    secret = paypal_client_secret    
    basic_auth = HTTPBasicAuth(client_id, secret)    
    headers = { "Content-Type": "application/json", }    
    response = requests.post(url=api_link, headers=headers, auth=basic_auth)
    

    if response.status_code != 201 and response.status_code != 200:
        #return redirect('/user/settings?status=Payment for library borrow with ID '+ str(borrow_id) + ' has been expired, no further process will occur.') 
        return jsonify({"status": "Payment for library borrow with ID " + str(borrow_id) + " has been expired, no further process will occur.", 'success': False}), 403
    captured_payment = response.json()
    if captured_payment['status'] == 'COMPLETED':
        borrow.hasResolved = True; db.session.commit()
        #return redirect('/user/settings?status=Thanks for your payment! Payment for library borrow with ID ' + str(borrow_id) + ' successfully!')
        return jsonify({"status": "Thanks for your payment! Payment for library borrow with ID " + str(borrow_id) + " successfully!", 'success': True}), 200
    else:
        return jsonify({"status": "Payment for library borrow with ID " + str(borrow_id) + " has been expired, no further process will occur.", 'success': False}), 403
        #return redirect('/user/settings?status=Payment for library borrow with ID '+ str(borrow_id) + ' has been expired, no further process will occur.') 
    

@library_settings_routes.route("/create-checkout-session/<borrow_id>", methods=['GET'])
def create_checkout_session(borrow_id):
    domain_url = server_domain
    stripe.api_key = stripe_secret_key
    if not check_user_authentication():
        return get_status_object_json(False, None, NOT_AUTHENTICATED), 403
    
    try:
        borrow_id = int(borrow_id)
    except:
        return get_status_object_json(False, None, INVALID_ID), 409
    
    borrow = db.session.query(BookBorrow).filter(BookBorrow.id == borrow_id).filter(BookBorrow.userId == current_user.id).first()
    if not borrow:
        return get_status_object_json(False, None, NOT_AUTHENTICATED), 403
    
    library_policies = get_policies()
    if library_policies != None:
        currency = library_policies[5]
    else:
        return get_status_object_json(False, None, DATABASE_ERROR), 500
    
    success, borrow_fee, error = get_borrow_fee(borrow_id, 0.0)
    if not success:
        #Borrow not approved or book hasn't returned/declared as lost or damaged
        return get_status_object_json(False, None, error), 409

    try:
        # Create new Checkout Session for the order
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + '/stripe-payment/' + str(borrow_id) + "/success" +  "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + "/stripe-payment/cancelled",
            payment_method_types=["card"],
            mode="payment",
            customer_creation="always",
            line_items=[
                {
                    "price_data": {
                        "currency": str(currency).lower(),
                        "product_data": {
                            "name": "Library Fee",
                        },
                        "unit_amount": convert_to_stripe(borrow_fee, str(currency).lower()),  # Amount in cents
                    },
                    "quantity": 1,
                }
            ]
        )
        #Since stripe.redirectToCheckout is deprecated, just return the checkout url instead
        #and let the frontend redirect to it
        return jsonify({"sessionId": checkout_session["id"], "url": checkout_session["url"]})
    except Exception as e:
        return get_status_object_json(False, None, error=str(e)), 403
    
@library_settings_routes.route('/stripe-payment/<borrow_id>/success')
def stripe_payment_success_callback(borrow_id):
    session = stripe.checkout.Session.retrieve(request.args.get('session_id'))
    status = session.get("status")
    borrow_id = int(borrow_id)
    
    if status == 'complete':
        set_borrow_resolve(borrow_id)
        return redirect('/user/settings?status=Thanks for your payment! Payment for library borrow with ID ' + str(borrow_id) + ' successfully!')
    elif status == 'open':
        set_borrow_resolve(borrow_id)
        return redirect('/user/settings?status=Payment for library borrow with ID '+ str(borrow_id) +
                         ' is still being processed, check your account and your bank later in cases of error.')
    
    else:
        return redirect('/user/settings?status=Payment for library borrow with ID '+ str(borrow_id) + ' has been expired, no further process will occur.')

@library_settings_routes.route("/stripe-payment/cancelled")
def stripe_payment_cancelled_callback():
    return redirect('/user/settings?status=Payment cancelled or failed.')

@library_settings_routes.route('/api/search-everything', methods=['GET'])
def search_everything():
    query = request.args.get('query')
    if query == None or query == '':
        return get_status_object_json(False, None, INVALID_PARAM), 400
    result = search_everything_controller(query)
    return get_status_object_json(True, result, None), 200

@library_settings_routes.route('/api/recent-events', methods=['GET'])
def get_recent_event():
    page = request.args.get('page')
    limit = request.args.get('limit')
    try:
        page = int(page) if page != None else 1
        limit = int(limit) if limit != None else 10
    except:
        return get_status_object_json(False, None, INVALID_PARAM), 400
    if page < 1 or limit < 1:
        return get_status_object_json(False, None, INVALID_PARAM), 400
    result = db.session.query(Article).filter(or_(Article.category.ilike('event'), Article.category.ilike('events'))). \
        order_by(desc(Article.date)).offset((page-1)*limit).limit(limit).all()
    return get_status_object_json(True, result, None), 200

@library_settings_routes.route('/api/search-event', methods=['GET'])
def search_event():
    page = request.args.get('page')
    limit = request.args.get('limit')
    query = request.args.get('query') if request.args.get('query') != None else ''
    if query != '':
        query = '%' + query + '%'
    try:
        page = int(page) if page != None else 1
        limit = int(limit) if limit != None else 10
    except:
        return get_status_object_json(False, None, INVALID_PARAM), 400
    if page < 1 or limit < 1:
        return get_status_object_json(False, None, INVALID_PARAM), 400
    result = db.session.query(Article).filter(or_(Article.category.ilike('event'), Article.category.ilike('events'))) \
        .filter(Article.title.like(query) | Article.content.like(query)) \
        .order_by(desc(Article.date)).offset((page-1)*limit).limit(limit).all()
    return get_status_object_json(True, result, None), 200


# REST methods for LibraryPlace
@library_settings_routes.route('/library/place', methods=['GET', 'POST'])
def places_route():
    if request.method == 'GET':
        
        places = db.session.query(LibraryPlace).all()
        available_places = []
        for place in places:
            sessionInUse = db.session.query(LibrarySession).filter_by(placeId=place.id, inUse=True).first()
            sessionInHold = db.session.query(LibrarySession).filter_by(placeId=place.id).first()
            available_places.append({
                'id': place.id,
                'room': place.room,
                'haveComputer': place.haveComputer,
                'isOnHold': sessionInHold != None,
                'isInUse': sessionInUse != None
            })
            
        return get_status_object_json(True, available_places, None), 200
    elif request.method == 'POST':
        room = request.form.get('room')
        has_computer = request.form.get('haveComputer')
        if has_computer == 'true' or has_computer == '1':
            has_computer = True
        else:
            has_computer = False
        
        place = LibraryPlace(room=room, haveComputer=has_computer)
        db.session.add(place)
        db.session.commit()
        return get_status_object_json(True, place, None), 200

@library_settings_routes.route('/library/place/<int:place_id>', methods=['PUT', 'DELETE'])
def place_route_put_delete(place_id):
    if request.method == 'PUT':
        place = db.session.query(LibraryPlace).filter(LibraryPlace.id == place_id).first()
        if place is None:
            return get_status_object_json(False, None, PLACE_NOT_FOUND), 404
        place.room = request.form.get('room')
        has_computer = request.form.get('haveComputer')
        if has_computer == 'true' or has_computer == '1':
            has_computer = True
        else:
            has_computer = False
        place.haveComputer = has_computer
        db.session.commit()
        return get_status_object_json(True, place, None), 200
    elif request.method == 'DELETE':
        place = db.session.query(LibraryPlace).filter(LibraryPlace.id == place_id).first()
        if place is None:
            return get_status_object_json(False, None, PLACE_NOT_FOUND), 404
        
        db.session.query(LibrarySession).filter(LibrarySession.placeId == place_id).delete()
        delete_row = db.session.query(LibraryPlace).filter(LibraryPlace.id == place_id).delete()
        if delete_row == 0:
            return get_status_object_json(False, None, UNRESOLVED_SESSION), 500
        db.session.commit()
        return get_status_object_json(True, None, None), 200

# REST methods for LibrarySession
@library_settings_routes.route('/library/session', methods=['GET'])
def get_all_sessions():
    sessions = db.session.query(LibrarySession).all()
    result = []
    for session in sessions:
        session_books = db.session.query(Book).join(LibrarySessionBook, LibrarySessionBook.bookId == Book.id).filter(LibrarySessionBook.sessionId == session.id).all()
        user = db.session.query(User).join(LibrarySession, LibrarySession.userId == User.id).filter(LibrarySession.id == session.id).first()
        session_books = [asdict(session_book) for session_book in session_books]
        session = asdict(session); user = asdict(user); session['books'] = session_books; session['user'] = user
        result.append(session)
    return get_status_object_json(True, result, None), 200

@library_settings_routes.route('/library/place/<int:place_id>/session', methods=['GET'])
def get_sessions_by_place_id(place_id):
    sessions = db.session.query(LibrarySession).filter(LibrarySession.placeId == place_id).all()
    result = []
    for session in sessions:
        session_books = db.session.query(Book).join(LibrarySessionBook, LibrarySessionBook.bookId == Book.id).filter(LibrarySessionBook.sessionId == session.id).all()
        user = db.session.query(User).join(LibrarySession, LibrarySession.userId == User.id).filter(LibrarySession.id == session.id).first()
        session_books = [asdict(session_book) for session_book in session_books]
        session = asdict(session); user = asdict(user); session['books'] = session_books; session['user'] = user
        result.append(session)
    return get_status_object_json(True, result, None), 200

@library_settings_routes.route('/library/session/<int:session_id>', methods=['GET'])
def get_session(session_id):
    session = db.session.query(LibrarySession).filter(LibrarySession.id == session_id).first()
    
    if session is None:
        return get_status_object_json(False, None, SESSION_NOT_FOUND), 404
    session_user = db.session.query(User).filter(User.id == session.userId).first()
    session_place = db.session.query(LibraryPlace).filter(LibraryPlace.id == session.placeId).first()
    session_books = db.session.query(Book).join(LibrarySessionBook, LibrarySessionBook.bookId == Book.id).filter(LibrarySessionBook.sessionId == session_id).all()
    session_books = [asdict(session_book) for session_book in session_books]
    session = asdict(session); session['books'] = session_books; session_user = asdict(session_user); session['user'] = session_user
    session_place = asdict(session_place); session['place'] = session_place
    return get_status_object_json(True, session, None), 200

@library_settings_routes.route('/library/session', methods=['POST'])
def add_session():
    place_id = request.form.get('placeId')
    user_id = request.form.get('userId')
    start_date = request.form.get('startDate')
    try:
        start_date = dateparse(start_date) if start_date != None else datetime.now()
        place_id = int(place_id)
        user_id = int(user_id)
    except:
        return get_status_object_json(False, None, INVALID_PARAM), 400
    session = LibrarySession(placeId=place_id, userId=user_id, startDate=start_date, inUse=False)
    db.session.add(session)
    db.session.commit()
    return get_status_object_json(True, session, None), 200

@library_settings_routes.route('/library/session/<int:session_id>', methods=['PUT'])
def update_session(session_id):
    session = db.session.query(LibrarySession).get(session_id)
    if session is None:
        return get_status_object_json(False, None, SESSION_NOT_FOUND), 404
    place_id = request.form.get('placeId')
    user_id = request.form.get('userId')
    start_date = request.form.get('startDate')
    in_use = request.form.get('inUse')
    try:
        place_id = int(place_id)
        user_id = int(user_id)
        start_date = dateparse(start_date) if start_date != None else datetime.now()
        in_use = True if in_use == 'true' or in_use == '1' else False
    except:
        return get_status_object_json(False, None, INVALID_PARAM), 400
    session.placeId = place_id
    session.userId = user_id
    session.startDate = start_date
    if session.inUse == False and in_use == True:
        session_books = db.session.query(LibrarySessionBook).filter(LibrarySessionBook.sessionId == session_id).all()
        for session_book in session_books:
            if session_book.book.stock == 0:
                return get_status_object_json(False, None, BOOK_OUT_OF_STOCK), 400
        db.session.query(Book).filter(Book.id.in_(session_books)).update({Book.stock: Book.stock - 1})
    if session.inUse == True and in_use == False:
        session_books = db.session.query(LibrarySessionBook.id).filter(LibrarySessionBook.sessionId == session_id).all()
        db.session.query(Book).filter(Book.id.in_(session_books)).update({Book.stock: Book.stock + 1})
    session.inUse = in_use

    db.session.commit()
    return get_status_object_json(True, session, None), 200

@library_settings_routes.route('/library/session/<int:session_id>', methods=['DELETE'])
def delete_session(session_id):
    session = db.session.query(LibrarySession).filter(LibrarySession.id == session_id).first()
    if session is None:
        return get_status_object_json(False, None, SESSION_NOT_FOUND), 404
    session_book_ids = db.session.query(LibrarySessionBook.bookId).filter(LibrarySessionBook.sessionId == session_id).all()
    db.session.query(Book).filter(Book.id.in_(session_book_ids)).update({Book.stock: Book.stock +1})
    db.session.query(LibrarySessionBook).filter(LibrarySessionBook.sessionId == session_id).delete()
    db.session.delete(session)
    db.session.commit()
    return get_status_object_json(True, None, None), 200

# REST methods for LibrarySessionBook
@library_settings_routes.route('/library/session/<int:session_id>/book', methods=['POST'])
def add_book_to_session(session_id):
    session = db.session.query(LibrarySession).filter(LibrarySession.id == session_id).first()
    if session is None:
        return get_status_object_json(False, None, SESSION_NOT_FOUND), 404
    book_id = request.form.get('bookId')
    try:
        book_id = int(book_id)
    except:
        return get_status_object_json(False, None, INVALID_PARAM), 400
    book = db.session.query(Book).filter(Book.id == book_id).first()
    if book is None:
        return get_status_object_json(False, None, INVALID_ID), 404
    if book.stock == 0 and session.inUse:
        return get_status_object_json(False, None, BOOK_OUT_OF_STOCK), 400
    if session.inUse:
        book.stock -= 1
    session_book = db.session.query(LibrarySessionBook).filter(LibrarySessionBook.sessionId == session_id, LibrarySessionBook.bookId == book_id).first()
    if session_book is None:
        return get_status_object_json(False, None, INVALID_ID), 404
    
    session_book = LibrarySessionBook(bookId=book_id, sessionId=session_id)
    db.session.add(session_book)
    db.session.commit()
    return get_status_object_json(True, session_book, None), 200

@library_settings_routes.route('/library/session/<int:session_id>/book', methods=['GET'])
def get_all_books(session_id):
    books = db.session.query(LibrarySessionBook).filter(LibrarySessionBook.sessionId == session_id).all()
    return get_status_object_json(True, books, None), 200

@library_settings_routes.route('/library/session/<int:session_id>/book/<int:book_id>', methods=['POST'])
def update_book_session(session_id, book_id):
    session = db.session.query(LibrarySession).filter(LibrarySession.id == session_id).first()
    if session is None:
        return get_status_object_json(False, None, SESSION_NOT_FOUND), 404
    try:
        book_id = int(book_id)
    except:
        return get_status_object_json(False, None, INVALID_PARAM), 400
    book = db.session.query(Book).filter(Book.id == book_id).first()

    if book == None:
        return get_status_object_json(False, None, INVALID_ID), 404
    if book.stock == 0 and session.inUse:
        return get_status_object_json(False, None, BOOK_OUT_OF_STOCK), 400
    session_book = db.session.query(LibrarySessionBook).filter(LibrarySessionBook.sessionId == session_id, LibrarySessionBook.bookId == book_id).first()
    
    if session.inUse:
        book.stock -= 1
    session_book = LibrarySessionBook(bookId=book_id, sessionId=session_id)
    db.session.add(session_book)
    db.session.commit()
    return get_status_object_json(True, session_book, None), 200


@library_settings_routes.route('/library/session/<int:session_id>/book/<int:book_id>', methods=['DELETE'])
def delete_book_session(session_id, book_id):
    session = db.session.query(LibrarySession).filter(LibrarySession.id == session_id).first()
    if session is None:
        return get_status_object_json(False, None, SESSION_NOT_FOUND), 404
    book = db.session.query(Book).filter(Book.id == book_id).first()
    if book is None:
        return get_status_object_json(False, None, INVALID_ID), 404
    session_book = db.session(LibrarySessionBook).filter(LibrarySessionBook.sessionId == session_id, LibrarySessionBook.bookId == book_id).first()
    if session_book is None:
        return get_status_object_json(True, None, None), 202
    if session.inUse:
        book.stock += 1
    db.session.delete(session_book)
    db.session.commit()
    return get_status_object_json(True, None, None), 200

@library_settings_routes.route('/library/session/<int:session_id>/in-use', methods=['POST', 'PUT'])
def set_session_in_use(session_id):
    session = db.session.query(LibrarySession).filter(LibrarySession.id == session_id).first()
    if session is None:
        return get_status_object_json(False, None, SESSION_NOT_FOUND), 404
    books = db.session.query(Book).join(LibrarySessionBook, LibrarySessionBook.bookId == Book.id).filter(LibrarySessionBook.sessionId == session_id).all()
    for book in books:
        if book.stock == 0:
            return get_status_object_json(False, None, BOOK_OUT_OF_STOCK), 409
    session.inUse = True
    for book in books:
        book.stock -= 1
    db.session.commit()
    return get_status_object_json(True, session, None), 200 

@library_settings_routes.route('/library/session/<int:session_id>/end', methods=['POST', 'PUT'])
def set_session_end(session_id):
    session = db.session.query(LibrarySession).filter(LibrarySession.id == session_id).first()
    if session is None:
        return get_status_object_json(False, None, SESSION_NOT_FOUND), 404
    if session.inUse:
        books = LibrarySessionBook.query.filter_by(sessionId=session_id).all()
        for book in books:
            book.book.stock += 1
    session.inUse = False
    db.session.commit()
    return get_status_object_json(True, None, None), 200