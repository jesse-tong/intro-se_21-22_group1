import csv
from dateutil.parser import parse as date_parse

#Function to format a time string to the format HH:mm:ss that SQLite can read
def sqlite_time_string_from_time_string(time_string):
    res = date_parse(time_string)
    t = res.strftime("%H:%M:%S")
    return t
