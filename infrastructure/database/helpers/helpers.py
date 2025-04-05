import pymongo
import mysql.connector
from sqlalchemy import MetaData
import os
from datetime import datetime, date
from infrastructure.config.config import (MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB_NAME, MONGO_DB_NAME,
                                          ALLOWED_TABLES, ALLOWED_EXTENSIONS, MONGO_CONFIG_STRING)


# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------

def get_tables():
    """
    Reads all tables from the relational database using automatic reflection.
    """
    from app import mysql_engine  # Import here to avoid circular dependency
    meta = MetaData()
    meta.reflect(bind=mysql_engine)
    return meta.tables.keys()


def get_mongo_client():
    """
    Returns a new MongoDB client instance.
    """
    return pymongo.MongoClient(MONGO_CONFIG_STRING)


def insert_message_to_mysql(message, duration):
    """
    Inserts a success or error message into the 'success_logs' table in MySQL.
    """
    try:

        conn = get_mysql_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO success_logs (message, duration)
            VALUES (%s, %s)
        """
        cursor.execute(query, (message, duration))
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error writing success message to MySQL: {err}")


def allowed_file(filename):
    """
    Checks whether the provided filename has an allowed extension (JSON).
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_mysql_connection():
    """
    Returns a new MySQL database connection.
    Use this function to avoid repeated connection setups.
    """
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB_NAME
    )


# Add this function to `helpers.py`
def get_db(table_name=""):
    """
    Returns a database connection based on the table name:
    - MySQL for relational tables
    - MongoDB for NoSQL collections
    """
    if table_name in ALLOWED_TABLES:
        return get_mysql_connection()
    else:
        # Return MongoDB collection for NoSQL collections
        mongo_client = get_mongo_client()
        db = mongo_client[os.getenv("MONGO_DB_NAME", "production")]
        return db[table_name]


def convert_to_mongodb(selected_tables, embed=True):
    """
    Converts specified tables from MySQL to MongoDB. If 'embed' is True, it embeds
    related data into a single 'embedded' collection; otherwise, each table is
    converted to its own MongoDB collection.
    """
    from app import mysql_engine, mysql_session

    client = pymongo.MongoClient(MONGO_CONFIG_STRING)
    db = client[MONGO_DB_NAME]

    session = mysql_session()
    meta = MetaData()
    meta.reflect(bind=mysql_engine)

    def fix_dates(data):
        """
        Converts datetime.date objects to datetime.datetime to ensure compatibility
        with MongoDB.
        """
        for key, value in data.items():
            if isinstance(value, date):
                data[key] = datetime(value.year, value.month, value.day)
        return data

    total_inserted = 0

    for table_name in selected_tables:
        if table_name not in meta.tables:
            print(f"Table {table_name} does not exist in the MySQL database.")
            continue

        table = meta.tables[table_name]
        query = session.query(table)
        rows = query.all()

        if embed:
            embedded_data = []
            for row in rows:
                row_dict = fix_dates(dict(row))
                embedded_data.append(row_dict)
            db["embedded"].insert_many(embedded_data)
            total_inserted += len(embedded_data)
        else:
            collection = db[table_name]
            documents = [fix_dates(dict(row)) for row in rows]
            collection.insert_many(documents)
            total_inserted += len(documents)

    session.close()
    print("Conversion completed.")
    return total_inserted
