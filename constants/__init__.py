import os
from dotenv import load_dotenv

load_dotenv()

DB_URI = os.getenv("DB_URI")
CONFIG_NAME = os.getenv("CONFIG_NAME")
SECRET_KEY = os.getenv("SECRET_KEY")
