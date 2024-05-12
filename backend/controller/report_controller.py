import os
borrow_time = os.environ.get('DEFAULT_BORROW_TIMEOUT')
overdue_fine = os.environ.get('OVERDUE_FINE_PER_DAY')
overdue_limit_before_treated_as_lost = os.environ.get('OVERDUE_DAYS_LIMIT_BEFORE_LOST')
damage_and_lost_fine = os.environ.get('DAMAGE_AND_LOST_FINE')
currency = os.environ.get('CURRENCY')

