import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from google.cloud import bigquery

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== Load environment variables ======
PG_HOST = os.environ["PG_HOST"]
PG_PORT = os.environ.get("PG_PORT", "5432")
PG_DB = os.environ["PG_DB"]
PG_USER = os.environ["PG_USER"]
PG_PASSWORD = os.environ["PG_PASSWORD"]

GCP_PROJECT_ID = os.environ["GCP_PROJECT_ID"]

# Dataset names
RAW_DATASET = "raw_data"
STAGING_DATASET = "staging_data"

# ====== SQLAlchemy Engine ======
db_url = URL.create(
    drivername="postgresql+psycopg2",
    username=PG_USER,
    password=PG_PASSWORD,   # SQLAlchemy will escape automatically
    host=PG_HOST,
    port=PG_PORT,
    database=PG_DB,
)
engine = create_engine(db_url)

# ====== BigQuery Client ======
bq_client = bigquery.Client(project=GCP_PROJECT_ID)
