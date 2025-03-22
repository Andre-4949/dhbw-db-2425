import os
from dotenv import load_dotenv
import pymongo

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB_NAME = os.getenv("MYSQL_DB_NAME")
MYSQL_DB_PORT = os.getenv("MYSQL_DB_PORT")

MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_PORT = os.getenv("MONGO_PORT")

MYSQL_CONFIG_STRING = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_DB_PORT}/{MYSQL_DB_NAME}"
MONGO_CONFIG_STRING = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/"

ALLOWED_EXTENSIONS = {'json'}

client = pymongo.MongoClient(MONGO_CONFIG_STRING)
db = client[MONGO_DB_NAME]

ALLOWED_TABLES = db.list_collection_names()

