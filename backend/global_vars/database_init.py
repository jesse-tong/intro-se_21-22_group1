import pymysql
from flask_sqlalchemy import SQLAlchemy
from multiprocessing import Value
import sqlite3

new_book_counter = Value('i', 0)
deleted_book_counter = Value('i', 0)

db = SQLAlchemy()

library_pols_db = sqlite3.connect('library_pols.db')

library_pols_db.execute('''create table if not exists LIB_POLICIES 
                        (ID INT PRIMARY KEY NOT NULL, 
                        DEFAULT_BORROW_TIME INT NOT NULL,
                        OVERDUE_FEE REAL NOT NULL,
                        OVERDUE_LIMIT INT NOT NULL,
                        DAMAGE_AND_LOST_FEE REAL NOT NULL,
                        CURRENCY TEXT NOT NULL,
                        OTHER_POLICIES TEXT NOT NULL
                        )''')

no_of_policies = library_pols_db.execute('SELECT COUNT(ID) FROM LIB_POLICIES').fetchone()[0]

if no_of_policies == 0:
    library_pols_db.execute("INSERT INTO LIB_POLICIES VALUES (1, 14, 3000, 30, 50000, 'VND', ' ')")

library_pols_db.commit()
library_pols_db.close()



