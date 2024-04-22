import pymssql
import pymysql
from flask_sqlalchemy import SQLAlchemy
from multiprocessing import Value

visit_counter = Value('i', 0)

db = SQLAlchemy()

