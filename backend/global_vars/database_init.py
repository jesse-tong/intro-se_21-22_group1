import pymysql
from flask_sqlalchemy import SQLAlchemy
from multiprocessing import Value
import sqlite3

new_book_counter = Value('i', 0)
deleted_book_counter = Value('i', 0)

db = SQLAlchemy()

policies_db_path = 'library_pols.db'

# Init the SQLite server that is used
library_pols_db = sqlite3.connect(policies_db_path)

library_pols_db.execute('''create table if not exists LIB_POLICIES 
                        (ID INT PRIMARY KEY NOT NULL, 
                        DEFAULT_BORROW_TIME INT NOT NULL,
                        OVERDUE_FEE REAL NOT NULL,
                        OVERDUE_LIMIT INT NOT NULL,
                        DAMAGE_AND_LOST_FEE REAL NOT NULL,
                        CURRENCY TEXT NOT NULL,
                        OTHER_POLICIES TEXT NOT NULL
                        )''')

library_pols_db.execute('''create table if not exists LIB_CONTACTS 
                        (ID INT PRIMARY KEY NOT NULL, 
                        ADDRESS TEXT,
                        PHONE_NUMBER TEXT,
                        EMAIL TEXT
                        )''')

#NORMAL_OPEN and NORMAL_CLOSE: open/close time in non-weekend days
#WEEKEND_OPEN and WEEKEND_CLOSE: open/close time in weekend days
#WEEKEND_START: start of weekend (greater than 1, Sunday is treated as 8, default 7)
#WEEKEND_END: end of weekend (greater than 1, Sunday is treated as 8, default 8)
library_pols_db.execute('''create table if not exists LIB_TIMINGS
                        (ID INT PRIMARY KEY NOT NULL,
                        NORMAL_OPEN TEXT NOT NULL,
                        NORMAL_CLOSE TEXT NOT NULL,
                        WEEKEND_OPEN TEXT NOT NULL,
                        WEEKEND_CLOSE TEXT NOT NULL,
                        WEEKEND_START INT NOT NULL CHECK (WEEKEND_START > 1 AND WEEKEND_START <= 8),
                        WEEKEND_END INT NOT NULL CHECK (WEEKEND_END > 1 AND WEEKEND_END <= 8 AND WEEKEND_START <= WEEKEND_END)
                        )''')

no_of_policies = library_pols_db.execute('SELECT COUNT(ID) FROM LIB_POLICIES').fetchone()[0]

no_of_contacts = library_pols_db.execute('SELECT COUNT(ID) FROM LIB_CONTACTS').fetchone()[0]

no_of_timings = library_pols_db.execute('SELECT COUNT(ID) FROM LIB_TIMINGS').fetchone()[0]

if no_of_policies == 0:
    library_pols_db.execute("INSERT INTO LIB_POLICIES VALUES (1, 14, 3000, 30, 50000, 'VND', ' ')")

if no_of_contacts == 0:
    library_pols_db.execute("INSERT INTO LIB_CONTACTS VALUES (1, '', '', '')")

if no_of_timings == 0:
    library_pols_db.execute("INSERT INTO LIB_TIMINGS VALUES (1, '9:00', '21:00', '10:00', '20:00', 7, 8)")

library_pols_db.commit()
library_pols_db.close()



