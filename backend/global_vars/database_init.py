import pymssql
import pymysql
from flask_sqlalchemy import SQLAlchemy
from multiprocessing import Value

new_book_counter = Value('i', 0)
deleted_book_counter = Value('i', 0)


db = SQLAlchemy()

