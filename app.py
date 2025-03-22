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
if __name__ == '__main__':
    app.run(debug=True)

