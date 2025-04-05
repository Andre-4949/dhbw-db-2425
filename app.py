import os
import logging
from dotenv import load_dotenv
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import infrastructure.config.config as config
from pymongo import MongoClient
import sqlalchemy
import shutil
from api.routes.route import register_routes

# -----------------------------------------------------------------------------
# Load Environment Variables
# -----------------------------------------------------------------------------
load_dotenv()

# -----------------------------------------------------------------------------
# Flask Application Setup
# -----------------------------------------------------------------------------
app = Flask(__name__, template_folder='web/templates', static_folder="static")
app.secret_key = os.getenv("SECRET_KEY")

# -----------------------------------------------------------------------------
# Logging Setup
# -----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

register_routes(app)
print(f"MYSQL_CONFIG_STRING: {config.MYSQL_CONFIG_STRING}")
print(f"MONGO_CONFIG_STRING: {config.MONGO_CONFIG_STRING}")
mysql_engine = create_engine(config.MYSQL_CONFIG_STRING)
mysql_session = sessionmaker(autocommit=False, autoflush=False, bind=mysql_engine)
# Set allowed tables for MySQL and MongoDB by listing them with SQL commands
# Fetch MySQL table names

# -----------------------------------------------------------------------------
# Main Entrypoint
# -----------------------------------------------------------------------------


#Um Datenbank zu erstellen und zu füllen


def execute_sql_script(file_path):
    with open(file_path, 'r') as file:
        sql_script = file.read()
    
    try:
        with mysql_engine.connect() as connection:
            for statement in sql_script.split(";"):
                if statement.strip():
                    print("STATEMENT: ", sqlalchemy.text(statement))
                    connection.execute(sqlalchemy.text(statement))
        print("✅ SQL-Skript erfolgreich ausgeführt!")
    except Exception as e:
        print(f"❌ Fehler beim Ausführen des SQL-Skripts: {e}")


def detect_end_of_line(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
        if b'\r\n' in content:
            return 'CRLF'
        elif b'\n' in content:
            return 'LF'
        elif b'\r' in content:
            return 'CR'
        else:
            return 'Unknown'

def check_and_convert_csv_files(directory):
    for filename in os.listdir(directory):
        if not filename.endswith('.csv'):
            continue
        file_path = os.path.join(directory, filename)
        end_of_line = detect_end_of_line(file_path)
        if end_of_line == 'CRLF':
            continue

        print(f"⚠️ Datei {filename} hat nicht das erwartete LF-Zeilenende. Konvertiere...")
        try:
            temp_file_path = file_path + ".tmp"
            with open(file_path, 'r', newline='') as infile, open(temp_file_path, 'w', newline='\r\n') as outfile:
                for line in infile:
                    outfile.write(line)
            shutil.move(temp_file_path, file_path)
            print(f"✅ Datei {filename} erfolgreich in das LF-Format konvertiert.")
        except Exception as e:
            print(f"❌ Fehler beim Konvertieren der Datei {filename}: {e}")
            exit(1)

check_and_convert_csv_files("data")


# execute_sql_script("data/create_mysql_db.sql")
# execute_sql_script("data/fill_mysql.sql")
if __name__ == '__main__':
    app.run(debug=True)


