from dotenv import load_dotenv, find_dotenv
import os

load_dotenv('./.env')

if os.environ.get('GOOGLE_CLIENT_ID') == None or os.environ.get('GOOGLE_CLIENT_SECRET') == None:
    raise EnvironmentError('GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET is not found, please check .env file')

if os.environ.get('STRIPE_PUBLISHABLE_KEY') == None or os.environ.get('STRIPE_SECRET_KEY') == None:
    raise EnvironmentError('STRIPE_PUBLISHABLE_KEY or STRIPE_SECRET_KEY is not found, please check the environment or .env file')

if os.environ.get('IP_TO_COUNTRY_DB') == None:
    raise EnvironmentError('IP_TO_COUNTRY_DB is not found, this is required for IP to country, please check the environment or .env file')

if os.environ.get('JWT_SECRET') == None:
    raise EnvironmentError('JWT_SECRET is not found, this is required for JWT, please check the environment or .env file')