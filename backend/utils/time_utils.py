import csv
from dateutil.parser import parse as date_parse
import maxminddb, os, json

ip_to_country_db = os.environ.get('IP_TO_COUNTRY_DB')
with open('./backend/instance/country-isocode.json') as f:
    iso3166_countries = json.load(f)

#Function to format a time string to the format HH:mm:ss that SQLite can read
def sqlite_time_string_from_time_string(time_string):
    res = date_parse(time_string)
    t = res.strftime("%H:%M:%S")
    return t

def ip_address_to_country(ip_addr: str) -> tuple[str, str | None, str] | None:
    with maxminddb.open_database(ip_to_country_db) as reader:
        try:
            ip_info = reader.get(ip_addr) 
            if ip_info != None:
                iso_alpha2 = ip_info.get('country').get('iso_code'); country = ip_info.get('country')['names']['en']
                iso_numeric = next((iso_data['country-code'] for iso_data in iso3166_countries 
                                    if iso_data.get('country-code') and iso_data['alpha-2'] == iso_alpha2), None)
                return iso_alpha2, iso_numeric, country
            else:
                return None #reader.get() will return None if ip address starts with 192.168.a.b or 127.a.b.c
        except ValueError:
            return None #Not a valid IPv4 or IPv6 address

