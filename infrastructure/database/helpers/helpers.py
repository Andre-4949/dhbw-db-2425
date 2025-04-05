import pymongo
import mysql.connector
from sqlalchemy import MetaData
import os
from datetime import datetime, date
from infrastructure.config.config import (
    MYSQL_HOST,
    MYSQL_USER,
    MYSQL_PASSWORD,
    MYSQL_DB_NAME,
    MONGO_DB_NAME,
    ALLOWED_EXTENSIONS,
    MONGO_CONFIG_STRING,
    MYSQL_ALLOWED_TABLES,
    MONGO_ALLOWED_TABLES,
)


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
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_mysql_connection():
    """
    Returns a new MySQL database connection.
    Use this function to avoid repeated connection setups.
    """
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB_NAME,
    )


# Add this function to `helpers.py`
def get_db(table_name=""):
    """
    Returns a database connection based on the table name:
    - MySQL for relational tables
    - MongoDB for NoSQL collections
    """
    if table_name in MYSQL_ALLOWED_TABLES:
        return get_mysql_connection()
    elif table_name in MONGO_ALLOWED_TABLES:
        # Return MongoDB collection for NoSQL collections
        mongo_client = get_mongo_client()
        db = mongo_client[os.getenv("MONGO_DB_NAME", "production")]
        return db[table_name]
    else:
        raise ValueError(
            f"Table {table_name} is not allowed in either MySQL or MongoDB."
        )


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
        # if table_name not in meta.tables:
        #     print(f"Table {table_name} does not exist in the MySQL database.")
        #     continue

        table = meta.tables[table_name]
        query = session.query(table)
        rows = query.all()
        column_names = table.columns.keys()
        rows_as_dicts = [dict(zip(column_names, row)) for row in rows]

        if embed and table_name == "Fahrt":
            embedded_data = []
            fks = table.foreign_keys
            if len(fks) == 0:
                print(f"Table {table_name} has no foreign keys.")
                continue
            # Pre-fetch all related data for foreign keys to minimize queries
            related_data_cache = {}
            for fk in fks:
                related_table = fk.column.table
                related_rows = session.query(related_table).all()
                related_data_cache[related_table.name] = {
                    row.id: fix_dates(dict(zip(related_table.columns.keys(), row)))
                    for row in related_rows
                }

            for row in rows_as_dicts:
                row_dict = fix_dates(row)
                for fk in fks:
                    # Match the foreign key column name
                    fk_column_name = fk.parent.name
                    related_table_name = fk.column.table.name
                    related_id = row.get(fk_column_name)

                    # Fetch the related row data from the cache
                    if related_id is not None:
                        related_row_dict = related_data_cache[related_table_name].get(related_id)
                        if related_row_dict:
                            # Replace the foreign key with the related row object
                            row_dict[related_table_name] = related_row_dict

                embedded_data.append(row_dict)

            # Remove duplicates based on '_id' field
            unique_embedded_data = {doc.get('_id', id(doc)): doc for doc in embedded_data}.values()

            db["embedded"].insert_many(unique_embedded_data)
            total_inserted += len(embedded_data)
        else:
            collection = db[table_name]
            documents = [fix_dates(row) for row in rows_as_dicts]
            collection.insert_many(documents)
            total_inserted += len(documents)

    session.close()
    print("Conversion completed.")
    return total_inserted
