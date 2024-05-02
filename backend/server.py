import os
import flask
import simplejson as json
from flask import Flask, request
from flask_cors import CORS
from global_vars.database_init import db
from global_vars.init_env import *
from flask_login import LoginManager
import pytest

print(os.environ.get('SQL_URL'))


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app
     , supports_credentials=True, origins = r"https?:\/\/(?:w{1,3}\.)?[^\s.]+(?:\.[a-z]+)*(?::\d+)?(?![^<]*(?:<\/\w+>|\/?>))",
     expose_headers=['X-CSRFToken'])
    
    
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=os.environ.get('SQL_URL'),
    )
    db.init_app(app)

    from models.user_model import User

    with app.app_context():
        db.create_all()


    login_manager = LoginManager()
    
    #Register login_manager to the main Flask so that login_manager and other
    #decorators such as current_user and login_required can be accessed by other blueprints
    login_manager.init_app(app=app)

    #This will manage which will be query and stored in current_user
    #Modify this if you want to store more information about user and session
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return db.session.query(User).filter(User.id == int(user_id)).first()

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # blueprint for auth routes in our app
    from routes.auth_routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from routes.comment_routes import comment_routes as comment_blueprint
    app.register_blueprint(comment_blueprint)

    from routes.book_routes import book_routes as book_blueprint
    app.register_blueprint(book_blueprint)

    from routes.book_user_routes import book_user as book_user_blueprint
    app.register_blueprint(book_user_blueprint)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

        

    return app

if __name__ == '__main__':
    from controller.user_controller import *
    from controller.book_controller import *
    from controller.book_user_controller import *
    from controller.comment_controller import *
    app = create_app()
    
    app.run(debug=True, use_reloader=True)
    