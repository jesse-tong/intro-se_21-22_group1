from dotenv import load_dotenv, find_dotenv
import os

dotenv_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.env')
load_dotenv(find_dotenv())