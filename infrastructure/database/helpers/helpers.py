from math import e
from flask.cli import F
import pymongo
import mysql.connector
from sqlalchemy import MetaData, Row, null
import os
from datetime import datetime, date
from typing import Any
from sqlalchemy.orm import Query
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
    return meta.tables


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
                    CREATE TABLE IF NOT EXISTS success_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                message TEXT NOT NULL,
                duration FLOAT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )"""
        cursor.execute(query)
        conn.commit()

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

def fix_dates(data):
    """
    Converts datetime.date objects to datetime.datetime to ensure compatibility
    with MongoDB.
    """
    for key, value in data.items():
        if isinstance(value, date):
            data[key] = datetime(value.year, value.month, value.day)
    return data

def convert_to_mongodb(selected_tables, embed=True):
    """
    Converts specified tables from MySQL to MongoDB. If 'embed' is True, it embeds
    related data into a single 'embedded' collection; otherwise, each table is
    converted to its own MongoDB collection.
    """
    from app import mysql_engine, mysql_session
    import json

    client = pymongo.MongoClient(MONGO_CONFIG_STRING)
    db = client[MONGO_DB_NAME]

    session = mysql_session()
    meta = MetaData()
    meta.reflect(bind=mysql_engine)
    print(selected_tables)
    
    total_inserted = 0
    for table_name in selected_tables:
        table = meta.tables[table_name]
        query = session.query(table)
        
        rows = query.all()
        column_names = table.columns.keys()
        rows_as_dicts = [dict(zip(column_names, row)) for row in rows]

        if embed and table_name == "Fahrt":
            embedded_data = []
            fahrzeug_table = meta.tables.get("Fahrzeug")
            geraet_table = meta.tables.get("Geraet")
            fahrt_fahrer_table = meta.tables.get("Fahrt_Fahrer")
            fahrer_table = meta.tables.get("Fahrer")
            fahrzeugparameter_table = meta.tables.get("Fahrzeugparameter")
            beschleunigung_table = meta.tables.get("Beschleunigung")
            diagnose_table = meta.tables.get("Diagnose")
            wartung_table = meta.tables.get("Wartung")
            geraet_installation_table = meta.tables.get("Geraet_Installation")

            # Pre-fetch related data to minimize database queries
            fahrzeug_data = {row.id: dict(zip(fahrzeug_table.columns.keys(), row)) for row in session.query(fahrzeug_table).all()} if fahrzeug_table is not None else {}
            geraet_data = {}
            if geraet_table is not None:
                for row in session.query(geraet_table).all():
                    row_dict = dict(zip(geraet_table.columns.keys(), row))
                    fahrzeug_id = row_dict.get("fahrzeugid")
                    if fahrzeug_id not in geraet_data.keys():
                        geraet_data[fahrzeug_id] = []
                    geraet = geraet_data[fahrzeug_id]
                    geraet.append(fix_dates(row_dict))
                    geraet_data[fahrzeug_id] = geraet
            # Group fahrt_fahrer data by Fahrt id
            fahrt_fahrer_data = {}
            if fahrt_fahrer_table is not None and fahrer_table is not None:
                fahrer_data = {row.id: dict(zip(fahrer_table.columns.keys(), row)) for row in session.query(fahrer_table).all()}
                for row in session.query(fahrt_fahrer_table).all():
                    ff_dict = dict(zip(fahrt_fahrer_table.columns.keys(), row))
                    fahrt_id = ff_dict.get("fahrtid")
                    fahrer_id = ff_dict.get("fahrerid")
                    if fahrt_id not in fahrt_fahrer_data.keys():
                        fahrt_fahrer_data[fahrt_id] = []
                    if fahrer_id in fahrer_data:
                        fahrer = fahrt_fahrer_data[fahrt_id]
                        fahrer.append(fix_dates(fahrer_data[fahrer_id]))
                        fahrt_fahrer_data[fahrt_id] = fahrer

            # Group related data properly based on correct keys
            fahrzeugparameter_data = {}
            if fahrzeugparameter_table is not None:
                for row in session.query(fahrzeugparameter_table).all():
                    key = getattr(row, "fahrtid")
                    d = dict(zip(fahrzeugparameter_table.columns.keys(), row))
                    d = fix_dates(d)
                    if key not in fahrzeugparameter_data.keys():
                        fahrzeugparameter_data[key] = []
                    parameter = fahrzeugparameter_data[key]
                    parameter.append(d)
                    fahrzeugparameter_data[key] = parameter
            beschleunigung_data = {}
            if beschleunigung_table is not None:
                for row in session.query(beschleunigung_table).all():
                    key = getattr(row, "fahrtid")
                    d = dict(zip(beschleunigung_table.columns.keys(), row))
                    d = fix_dates(d)
                    if key not in beschleunigung_data.keys():
                        beschleunigung_data[key] = []
                    existing_beschleunigung = beschleunigung_data[key]
                    existing_beschleunigung.append(d)
                    beschleunigung_data[key] = existing_beschleunigung

            diagnose_data = {}
            if diagnose_table is not None:
                for row in session.query(diagnose_table).all():
                    key = getattr(row, "fahrtid")
                    d = dict(zip(diagnose_table.columns.keys(), row))
                    d = fix_dates(d)
                    if key not in diagnose_data.keys():
                        diagnose_data[key] = []
                    existing_diagnose = diagnose_data[key]
                    existing_diagnose.append(d)
                    diagnose_data[key] = existing_diagnose

            wartung_data = {}
            if wartung_table is not None:
                for row in session.query(wartung_table).all():
                    key = getattr(row, "fahrzeugid")
                    d = dict(zip(wartung_table.columns.keys(), row))
                    d = fix_dates(d)
                    if key not in wartung_data.keys():
                        wartung_data[key] = []
                    existing_wartung = wartung_data[key]
                    existing_wartung.append(d)
                    wartung_data[key] = existing_wartung    

            geraet_installation_data = {}
            if geraet_installation_table is not None:
                for row in session.query(geraet_installation_table).all():
                    key = getattr(row, "fahrzeugid")
                    d = dict(zip(geraet_installation_table.columns.keys(), row))
                    d = fix_dates(d)
                    if key not in geraet_installation_data.keys():
                        geraet_installation_data[key] = []
                    existing_geraet_installation = geraet_installation_data[key]
                    existing_geraet_installation.append(d)
                    geraet_installation_data[key] = existing_geraet_installation
            
            print(json.dumps(geraet_installation_data,indent=4, default=str))    
            for row in rows_as_dicts:
                row_dict = fix_dates(row)
                row_dict["fahrzeug"] = fix_dates(fahrzeug_data.get(row_dict.get("fahrzeugid"), {}))
                row_dict["fahrer"] = fahrt_fahrer_data.get(row_dict.get("id"), [])
                row_dict["fahrzeugparameter"] = fahrzeugparameter_data.get(int(row_dict.get("id",-1)), {})
                row_dict["beschleunigung"] = beschleunigung_data.get(row_dict.get("id"), {})
                row_dict["diagnose"] = diagnose_data.get(row_dict.get("id"), [])
                row_dict["wartung"] = wartung_data.get(row_dict.get("fahrzeugid"), [])
                row_dict["geraet_installation"] = geraet_installation_data.get(row_dict.get("fahrzeugid"), [])
                currently_installed = []
                for geraet_intallation in row_dict["geraet_installation"]:
                    geraet_id = geraet_intallation.get("geraetid")
                    if geraet_intallation.get("einbau_datum") is not null and geraet_intallation.get("ausbau_datum") is null:
                        currently_installed.append(geraet_id)
                row_dict["geraet"] = [fix_dates(geraet) if geraet.get("id") in currently_installed else None for geraet in geraet_data.get(row_dict.get("fahrzeugid"), []) ]
                embedded_data.append(row_dict)

            db["embedded"].insert_many(list(embedded_data))
            total_inserted += len(embedded_data)
        else:
            collection = db[table_name]
            documents = [fix_dates(row) for row in rows_as_dicts]
            if len(documents) != 0:
                collection.insert_many(documents)
                total_inserted += len(documents)

    session.close()
    print("Conversion completed.")
    return total_inserted