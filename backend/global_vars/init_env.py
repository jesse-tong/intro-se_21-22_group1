from dotenv import load_dotenv, find_dotenv
import os

load_dotenv('./.env')

if os.environ.get('GOOGLE_CLIENT_ID') == None or os.environ.get('GOOGLE_CLIENT_SECRET') == None:
    raise EnvironmentError('GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET is not found, please check .env file')
