from flask import Blueprint, url_for, request, make_response
from models.user_model import User, Comment
from global_vars.database_init import db
from models.book_model import Book
from controller.comment_controller import *
from controller.user_controller import get_current_user_role
from utils.get_status_object import get_status_object_json
from flask_login import current_user
from flask_cors import CORS

comment_routes = Blueprint('comment_routes', __name__)
CORS(comment_routes, supports_credentials=True, origins = r"https?:\/\/(?:w{1,3}\.)?[^\s.]+(?:\.[a-z]+)*(?::\d+)?(?![^<]*(?:<\/\w+>|\/?>))",
    expose_headers=['X-CSRFToken'])

@comment_routes.route('/api/comment/<book_id>', methods=['GET'])
def get_book_comments_route(book_id):
    page = request.args.get('page')
    limit = request.args.get('limit')
    try:
        book_id = int(book_id)
        page = int(page) if page != None else None
        limit = int(limit) if limit != None else None
    except:
        return get_status_object_json(False, None, INVALID_ID), 400
    
    success, search_result, error = get_book_comment(book_id, page*limit, limit)
    
    return get_status_object_json(success, search_result, error), 200

@comment_routes.route('/api/comment', methods=['GET', 'POST', 'PUT', 'DELETE'])
def comment_action_api():
    find_role_success, role, error = get_current_user_role()
    if request.method == 'GET':
        user_id = request.args.get('user_id')
        page = request.args.get('page')
        limit = request.args.get('limit')
        try:
            user_id = int(user_id)
            page = int(page) if page != None else None
            limit = int(limit) if limit != None else None
        except:
            return get_status_object_json(False, None, INVALID_ID), 400
        success, search_result, error = get_user_comment(user_id, page*limit, limit)
        return get_status_object_json(success, result, error), 200
    elif request.method == 'POST':
        if current_user.is_authenticated:
            user_id = current_user.id 
            book_id = request.form.get('book_id')
            comment = request.form.get('comment')
            rating = request.form.get('rating')
            success, result, error = add_comment(user_id, book_id, comment, rating)
            return get_status_object_json(success, result, error), 200
        else:
            return get_status_object_json(False, None, NOT_AUTHENTICATED), 403
    elif request.method == 'PUT':
        if current_user.is_authenticated:
            user_id = int(current_user.id)
            comment_id = request.form.get('comment_id')
            comment = request.form.get('comment')
            rating = request.form.get('rating')
            try:
                comment_id = int(comment_id)
            except:
                return  get_status_object_json(False, None, INVALID_ID), 400
            comment = db.session.query(Comment).filter(Comment.id == comment_id).first()
            #Not enough permission
            if (role == None or (role != 'admin' and role != 'staff')) and comment.userId != user_id:
                return get_status_object_json(False, None, NOT_AUTHENTICATED), 403
            else:
                success, result, error = edit_comment(comment_id, comment, rating)
                return get_status_object_json(success, result, error), 200
    elif request.method == 'DELETE':
        comment_id = request.form.get('comment_id')
        try:
            comment_id = int(comment_id)
        except:
            return  get_status_object_json(False, None, INVALID_ID), 400
        comment = db.session.query(Comment).filter(Comment.id == comment_id).first()
        #Not enough permission
        if (role == None or (role != 'admin' and role != 'staff')) and comment.userId != user_id:
            return get_status_object_json(False, None, NOT_AUTHENTICATED), 403
        else:
            success, result, error = delete_comment(comment_id)
            return get_status_object_json(success, result, error), 200

