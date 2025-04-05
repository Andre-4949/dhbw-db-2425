from pymongo.errors import OperationFailure
import sqlalchemy
import os
from dotenv import load_dotenv
import pymongo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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

mysql_engine = create_engine(MYSQL_CONFIG_STRING)
mysql_session = sessionmaker(autocommit=False, autoflush=False, bind=mysql_engine)
with mysql_engine.connect() as connection:
    result = connection.execute(sqlalchemy.text("SHOW TABLES;"))
MYSQL_ALLOWED_TABLES = [row[0] for row in result]

# Fetch MongoDB collection names

mongo_client = pymongo.MongoClient(MONGO_CONFIG_STRING)
mongo_db = mongo_client.get_database(MONGO_DB_NAME)
MONGO_ALLOWED_TABLES = mongo_db.list_collection_names()

for collection in MONGO_ALLOWED_TABLES:
    try:
        mongo_db.drop_collection(collection)
    except OperationFailure as e:
        print(f"Error dropping collection {collection}: {e}")
print("All mongo collections dropped successfully. Comment this out in config.py if you want to keep the collections.")