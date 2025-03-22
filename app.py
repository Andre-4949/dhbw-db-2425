import os
import logging
from dotenv import load_dotenv
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infrastructure.config.config import MYSQL_CONFIG_STRING

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

from api.routes.route import MONGO_CONFIG_STRING, register_routes
register_routes(app)
print(f"MYSQL_CONFIG_STRING: {MYSQL_CONFIG_STRING}")
print(f"MONGO_CONFIG_STRING: {MONGO_CONFIG_STRING}")
mysql_engine = create_engine(MYSQL_CONFIG_STRING)
mysql_session = sessionmaker(autocommit=False, autoflush=False, bind=mysql_engine)
# -----------------------------------------------------------------------------
# Main Entrypoint
# -----------------------------------------------------------------------------


#Um Datenbank zu erstellen und zu füllen

# import sqlalchemy

# def execute_sql_script(file_path):
#     with open(file_path, 'r') as file:
#         sql_script = file.read()
    
#     try:
#         with mysql_engine.connect() as connection:
#             for statement in sql_script.split(";"):
#                 if statement.strip():
#                     print("STATEMENT: ", sqlalchemy.text(statement))
#                     connection.execute(sqlalchemy.text(statement))
#         print("✅ SQL-Skript erfolgreich ausgeführt!")
#     except Exception as e:
#         print(f"❌ Fehler beim Ausführen des SQL-Skripts: {e}")



# execute_sql_script("./data/create_mysql_db.sql")
# execute_sql_script("./data/fill_mysql.sql")

if __name__ == '__main__':
    app.run(debug=True)


