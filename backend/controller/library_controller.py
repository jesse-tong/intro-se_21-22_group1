import sqlite3
from global_vars.errors import *
from dataclasses import asdict
from global_vars.constants import *

def update_policies(default_borrow_time: int=None, overdue_fine_per_day: float=None, 
                    overdue_limit: int=None, damage_lost_fine: float = None, new_currency: str=None, other_policies: str=None):
    query = 'UPDATE LIB_POLICIES SET {} WHERE ID = 1'
    set_str = []
    if default_borrow_time != None:
        set_str.append('DEFAULT_BORROW_TIME = ' + str(default_borrow_time))
    if overdue_fine_per_day != None:
        set_str.append('OVERDUE_FEE = ' + str(overdue_fine_per_day))
    if overdue_limit != None:
        set_str.append('OVERDUE_LIMIT = ' + str(overdue_limit))
    if damage_lost_fine != None:
        set_str.append('DAMAGE_AND_LOST_FEE = ' + str(damage_lost_fine))
    if new_currency != None:
        set_str.append("CURRENCY = '{}'".format(str(new_currency)))
    if other_policies != None:
        set_str.append("OTHER_POLICIES = '{}'".format(str(other_policies)))

    query = query.format(', '.join(set_str))
    with sqlite3.connect('library_pols.db') as connection:
        try:
            connection.execute(query)
            connection.commit()
        except sqlite3.Error as er:
            return False, er.sqlite_errorcode
    
    return True, None

def update_library_contacts(address: str=None, phone_number: str=None, email: str=None):
    query = 'UPDATE LIB_CONTACTS SET {} WHERE ID = 1'
    set_str = []

    if address != None:
        set_str.append("ADDRESS = '{}'".format(str(address)))
    if phone_number != None:
        set_str.append("PHONE_NUMBER = '{}'".format(str(phone_number)))
    if email != None:
        set_str.append("EMAIL = '{}'".format(str(email)))

    query = query.format(', '.join(set_str))
    with sqlite3.connect('library_pols.db') as connection:
        try:
            connection.execute(query)
            connection.commit()
        except sqlite3.Error as er:
            return False, er.sqlite_errorcode
    
    return True, None

def get_policies():
    with sqlite3.connect('library_pols.db') as connection:
        try:
            policies = connection.execute('SELECT * FROM LIB_POLICIES WHERE ID = 1').fetchone()
            return policies
        except:
            return None
        
def get_library_contacts():
    with sqlite3.connect('library_pols.db') as connection:
        try:
            contacts = connection.execute('SELECT * FROM LIB_CONTACTS WHERE ID = 1').fetchone()
            return contacts
        except:
            return None