from flask import Blueprint, request, send_file
from werkzeug.datastructures import FileStorage
from models.user_model import User, Comment
from global_vars.database_init import db
from models.book_model import Book, BookAuthor, BookGenre
from sqlalchemy import func, distinct
import json, uuid
from flask_login import current_user
from flask_cors import CORS
from controller.book_controller import *
from controller.user_controller import get_current_user_role
from controller.comment_controller import get_book_avg_rating
from global_vars.constants import status_template, result_per_page
from utils.get_status_object import get_status_object_json

book_routes = Blueprint('book_routes', __name__)
CORS(book_routes, supports_credentials=True, origins = r"https?:\/\/(?:w{1,3}\.)?[^\s.]+(?:\.[a-z]+)*(?::\d+)?(?![^<]*(?:<\/\w+>|\/?>))",
    expose_headers=['X-CSRFToken'])

@book_routes.route('/hello-world', methods=['GET'])
def hello_world_route():
    return 'Hello world!', 200

# GET: Search book, POST: add book (admin only), PUT: edit book, 
@book_routes.route('/api/book', methods=['GET', 'POST', 'PUT', 'DELETE'])
def get_and_add_book_route():
    if request.method == 'GET':
        page = request.args.get('page')
        start_publish = request.args.get('start_publish') #Publish year search start
        end_publish = request.args.get('end_publish') #Publish year search end
        book_id = request.args.get('book_id')
        limit = request.args.get('limit')
        try:
            page = int(page) if page != None else None
            limit = int(limit) if limit != None else None
            book_id = int(book_id) if book_id != None else None
            start_publish = int(start_publish) if start_publish != None else None
            end_publish = int(end_publish) if end_publish != None else None
        except:
            status = status_template
            return get_status_object_json(False, None, INVALID_PARAM), 400
        title = request.args.get('title')
        isbn = request.args.get('isbn')
        if page != None:
            start_from = (page - 1)*result_per_page
        else:
            start_from = None
        description = request.args.get('description')
        result, query_result, error = search_book(title, start_publish, end_publish,
 description, start_from=start_from, limit=limit, isbn=isbn, book_id=book_id)

        return get_status_object_json(result, query_result, error), 200
    
    elif request.method == 'POST':
        result, role, error = get_current_user_role()
        if result == False or role != 'admin':
            status = get_status_object_json(False, None, error)
            return status, 200
        
        book_data = request.form
        print(book_data)
        title = book_data.get('title');
        publish_year = book_data.get('publish_year'); description = book_data.get('description')
        isbn = book_data.get('isbn'); authors = book_data.get('authors'); genres = book_data.get('genres')
        stock = book_data.get('stock'); languages = book_data.get('languages')
        if title == None:
            return get_current_user_role(False, None, INVALID_PARAM), 400
        try:
            publish_year = int(publish_year) if publish_year != None else None
            authors = json.loads(authors) if authors != None else list()
            genres = json.loads(genres) if genres != None else list()
            languages = json.loads(languages) if languages != None else list()
            stock = int(stock) if stock != None or stock != 0 else 0
        except:
            return get_status_object_json(False, None, INVALID_PARAM), 400
        
        success, new_book, error = add_book(title, publish_year, description, isbn)
        
        if authors == None and genres == None:
            return get_status_object_json(success, new_book, error), 200
        else:
            #If also add authors and genres, add them too
            if success == True:
                success, updated, error = change_book_data(new_book.id, authors=authors, genres=genres, description=description, isbn=isbn, stock=stock, languages=languages)
                return get_status_object_json(success, new_book, error), 200
            else:
                return get_status_object_json(False, None, ADD_ENTRY_ERROR), 500
        
    elif request.method == 'PUT':
        result, role, error = get_current_user_role()
        if result == False or role != 'admin':
            status = get_status_object_json(False, None, error)
            return status, 200
        book_data = request.form
        book_id = book_data.get('id'); title = book_data.get('title');
        publish_year = book_data.get('publish_year'); description = book_data.get('description')
        authors = book_data.get('authors') #Author should be a JSON string from an array
        genres = book_data.get('genres'); isbn = book_data.get('isbn')
        stock = book_data.get('stock'); languages = book_data.get('languages')
        try:
            book_id = int(book_id)
            publish_year = int(publish_year)
            authors = list(json.loads(authors)) if authors != None else list()
            genres = list(json.loads(genres))  if genres != None else list()
            languages = list(json.loads(languages)) if languages != None else list()
            stock = int(stock) if stock != None else 0
        except:
            return get_status_object_json(False, None, INVALID_PARAM), 400
        success, edited_data, error = change_book_data(book_id, title, publish_year, description, authors, genres, isbn, stock, languages)
        return get_status_object_json(success, edited_data, error), 200
    elif request.method == 'DELETE':
        bookId = request.form.get('book_id')
        try:
            id = int(bookId)
        except:
            error_status = get_status_object_json(False, None, INVALID_PARAM)
            return error_status, 400
        
        success, status, error = delete_book(id)
        return get_status_object_json(success, status, error), 200


@book_routes.route('/api/book/<bookId>', methods=['GET', 'PUT', 'DELETE'])
def edit_delete_book_route(bookId):
    if request.method == 'GET':
        try:
            book_id = int(bookId)
        except:
            return get_status_object_json(False, None, INVALID_PARAM), 400
        
        success, data, error = get_book_data(book_id)
        return get_status_object_json(success, data, error)
    elif request.method == 'PUT':
        try:
            id = int(bookId)
        except:
            error_status = get_status_object_json(False, None, INVALID_ID)
            return error_status, 400
        
        """ result, role, error = get_current_user_role()
        if result == False or role != 'admin':
            status = get_status_object_json(False, None, error)
            return status, 200 """
        book_data = request.form
        title = book_data.get('title');
        publish_year = book_data.get('publish_year'); description = book_data.get('description')
        authors = book_data.get('authors') #Author should be a JSON string from an array
        genres = book_data.get('genres'); isbn = book_data.get('isbn')
        stock = book_data.get('stock')
        try:
            publish_year = int(publish_year)
            stock = int(stock) if stock != None else 0
            authors = list(json.loads(authors)) if authors != None else list()
            genres = list(json.loads(genres))  if genres != None else list()
        except:
            return get_status_object_json(False, None, INVALID_PARAM), 400
        success, edited_data, error = change_book_data(id, title, publish_year, description, authors, genres, isbn, stock)
        return get_status_object_json(success, edited_data, error), 200
    elif request.method == 'DELETE':
        try:
            id = int(bookId)
        except:
            error_status = get_status_object_json(False, None, INVALID_ID)
            return error_status, 400
        
        success, status, error = delete_book(id)
        return get_status_object_json(success, status, error), 200
        
@book_routes.route('/api/upload-image/<book_id>', methods=['POST'])
def upload_book_image(book_id):
    if request.method == 'POST':
        try:
            book_id = int(book_id)
        except:
            return get_status_object_json(False, None, INVALID_PARAM), 400
        book = db.session.query(Book).filter(Book.id == book_id).first()
        if not book:
            return get_status_object_json(False, None, INVALID_ID), 400
        file = request.files.get('image')
        if not file:
            return get_status_object_json(False, None, NO_FILE_UPLOADED), 400
        image_bytes = file.read()
        save_book_image(image_bytes, book_id, 'main_image')
        return get_status_object_json(True, True, None)
    
@book_routes.route('/image/<book_id>', methods=['GET'])
def get_book_image(book_id):
    if request.method == 'GET':
        try:
            book_id = int(book_id)
        except:
            return get_status_object_json(False, None, INVALID_PARAM), 404
        book = db.session.query(Book).filter(Book.id == book_id).first()
        if not book:
            return get_status_object_json(False, None, INVALID_ID), 404
        image_path = os.path.join(os.path.abspath(os.environ.get('IMAGE_STORAGE_PATH')), str(book_id))
        image_path = os.path.join(image_path, 'main_image')
        if os.path.isfile(image_path):
            return send_file(image_path, as_attachment=False), 200
        else:
            return get_status_object_json(False, None, NO_FILE_UPLOADED), 404
        
@book_routes.route('/api/book-location', methods=['GET', 'POST', 'PUT', 'DELETE'])
def book_location_route():
    if request.method == 'GET':
        book_id = request.args.get('book_id')
        try:
            book_id = int(book_id)
        except:
            return get_status_object_json(False, None, INVALID_PARAM), 400
        
        success, result, error = get_book_location(book_id)
        return get_status_object_json(success, result, error)
    elif request.method == 'POST':
        book_id = request.form.get('book_id')
        shelf_id = request.form.get('shelf_id')
        room_id = request.form.get('room_id')
        try:
            book_id = int(book_id)
        except:
            return get_status_object_json(False, None, INVALID_PARAM), 400
        
        success, result, error = add_book_location(book_id, room_id, shelf_id)
        return get_status_object_json(success, result, error), 200
    elif request.method == 'PUT':
        book_location_id = request.form.get('book_location_id')
        shelf_id = request.form.get('shelf_id')
        room_id = request.form.get('room_id')
        try:
            book_location_id = int(book_location_id)
        except:
            return get_status_object_json(False, None, INVALID_PARAM), 400
        
        success, result, error = change_book_location(book_location_id, room_id, shelf_id)
        return get_status_object_json(success, result, error)
    elif request.method == 'DELETE':
        book_location_id = request.form.get('book_location_id')
        try:
            book_location_id = int(book_location_id)
        except:
            return get_status_object_json(False, None, INVALID_PARAM), 400
        success, result, error = delete_book_location(book_location_id)
        return get_status_object_json(success, result, error), 200

@book_routes.route('/api/get-genres', methods=['GET'])
def get_genres_api():
    page = request.args.get('page')
    limit = request.args.get('limit')
    try:
        page = int(page) if page != None else None; limit= int(limit) if limit != None else None
    except:
        return get_status_object_json(False, None, INVALID_PARAM), 400
    success, genres, error = get_genres(page, limit)
    return get_status_object_json(success, genres, error), 200

@book_routes.route('/api/get-authors', methods=['GET'])
def get_authors_api():
    page = request.args.get('page')
    limit = request.args.get('limit')
    try:
        page = int(page) if page != None else None; limit= int(limit) if limit != None else None
    except:
        return get_status_object_json(False, None, INVALID_PARAM), 400
    success, authors, error = get_authors(page, limit)
    return get_status_object_json(success, authors, error), 200

@book_routes.route('/api/author/<author_id>/books', methods=['GET'])
def get_books_of_author(author_id):
    page = request.args.get('page')
    limit = request.args.get('limit')
    try:
        author_id = int(author_id)
        page = int(page) if page != None else None; limit= int(limit) if limit != None else None
    except:
        return get_status_object_json(False, None, INVALID_PARAM), 400

    success, books, error = get_books_author(author_id, page, limit)
    return get_status_object_json(success, books, error), 200

@book_routes.route('/api/genre/<genre_id>/books', methods=['GET'])
def get_books_of_genre(genre_id):
    page = request.args.get('page')
    limit = request.args.get('limit')
    try:
        genre_id = int(genre_id) if genre_id != None else None
        page = int(page) if page != None else None; limit= int(limit) if limit != None else None
    except:
        return get_status_object_json(False, None, INVALID_PARAM), 400

    success, books, error = get_books_genre(genre_id, page, limit)
    return get_status_object_json(success, books, error), 200

@book_routes.route('/api/book-count', methods=['GET'])
def book_count():
    try:
        book_counts = db.session.query(func.count(distinct(Book.id))).first()
        return get_status_object_json(True, book_counts[0], None), 200
    except:
        return get_status_object_json(False, None, DATABASE_ERROR), 500
    
@book_routes.route('/api/book-average-rating/<book_id>', methods=['GET'])
def get_avg_book_rating(book_id):
    try:
        book_id = int(book_id)
    except:
        return get_status_object_json(False, None, INVALID_PARAM), 400
    success, result, error = get_book_avg_rating(book_id)
    return get_status_object_json(success, result, error)

@book_routes.route('/api/advanced-search', methods=['GET'])
def advanced_search_route():
    book_data = request.args.to_dict(flat=False)
    print(book_data)
    book_id = book_data.get('book_id'); title = book_data.get('title');
    publish_year = book_data.get('publish_year'); description = book_data.get('description')
    authors = book_data.get('authors[]') #Author should be a JSON string from an array
    genres = book_data.get('genres[]'); isbn = book_data.get('isbn')
    page = book_data.get('page'); limit = book_data.get('limit')
    print(authors); print(genres); print(type(genres))
    try:
        book_id = int(book_id[0]) if book_id != None else None
        publish_year = int(publish_year[0]) if publish_year != None else None
        authors = authors if authors != None else None
        genres = genres  if genres != None else None
        page = int(page[0]) if page != None else None
        limit = int(limit[0]) if limit != None else None
        description = description[0] if description != None else None
        title = title[0] if title != None else None
        isbn = isbn[0] if isbn != None else None
    except:
        return get_status_object_json(False, None, INVALID_PARAM), 400
    
    if page != None and limit != None and (page <= 0 or limit <= 0):
        return get_status_object_json(False, None, INVALID_PARAM), 400
    
    success, edited_data, error = advanced_search(book_id, title, publish_year, description, authors, genres, isbn, page, limit)
    return get_status_object_json(success, edited_data, error), 200