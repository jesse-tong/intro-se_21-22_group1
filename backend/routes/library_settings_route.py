from flask import Blueprint, request, jsonify, render_template_string, redirect
from global_vars.database_init import db
from sqlalchemy import func, distinct
import json, uuid, stripe
from flask_login import current_user
from flask_cors import CORS
from controller.library_controller import *
from controller.book_user_controller import get_borrow_fee, delete_borrow
from models.user_book import BookBorrow
from global_vars.constants import status_template, result_per_page
from utils.get_status_object import get_status_object_json
from utils.file_utils import *
from controller.book_user_controller import currency

#Blue print for miscellanous library settings
library_settings_routes = Blueprint('library_settings_routes', __name__)
CORS(library_settings_routes, supports_credentials=True, origins = r"https?:\/\/(?:w{1,3}\.)?[^\s.]+(?:\.[a-z]+)*(?::\d+)?(?![^<]*(?:<\/\w+>|\/?>))", expose_headers=['X-CSRFToken'])

stripe_publishable_key = os.environ.get('STRIPE_PUBLISHABLE_KEY')
stripe_secret_key = os.environ.get('STRIPE_SECRET_KEY')
server_domain = os.environ.get('VITE_API_POINT')

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
        success, edited_article, error = edit_article(article_id, title, content)
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
        success, added_article, error = add_article(title, content)
        return get_status_object_json(success, added_article, error), 200
    
@library_settings_routes.route('/get-stripe-key')
def get_stripe_publishable_key():
    stripe_config = {"publicKey": stripe_publishable_key}
    return jsonify(stripe_config)

@library_settings_routes.route("/create-checkout-session/<borrow_id>", methods=['GET'])
def create_checkout_session(borrow_id):
    domain_url = server_domain
    stripe.api_key = stripe_secret_key
    if not current_user.is_authenticated:
        return get_status_object_json(False, None, NOT_AUTHENTICATED), 403
    
    try:
        borrow_id = int(borrow_id)
    except:
        return get_status_object_json(False, None, INVALID_ID), 409
    
    borrow = db.session.query(BookBorrow).filter(BookBorrow.id == borrow_id).filter(BookBorrow.userId == current_user.id).first()
    if not borrow:
        return get_status_object_json(False, None, NOT_AUTHENTICATED), 403

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
        delete_borrow(borrow_id)
        return redirect('/user/settings?status=Thanks for your payment! Payment for library borrow with ID ' + str(borrow_id) + ' successfully!')
    elif status == 'open':
        delete_borrow(borrow_id)
        return redirect('/user/settings?status=Payment for library borrow with ID '+ str(borrow_id) +
                         ' is still being processed, check your account and your bank later in cases of error.')
    else:
        return redirect('/user/settings?status=Payment for library borrow with ID '+ str(borrow_id) + ' has been expired, no further process will occur.')

@library_settings_routes.route("/stripe-payment/cancelled")
def stripe_payment_cancelled_callback():
    return redirect('/user/settings?status=Payment cancelled or failed.')