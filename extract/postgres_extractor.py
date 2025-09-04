import pandas as pd
import logging
from config.settings import engine

logger = logging.getLogger(__name__)

def extract_from_postgres(last_updated=None):
    """Extract incrementally from Postgres users table"""
    if last_updated:
        sql = f"""
        SELECT * FROM users 
        WHERE updated_at > '{last_updated}'
        ORDER BY updated_at
        """
    else:
        sql = "SELECT * FROM users ORDER BY updated_at"

    df = pd.read_sql(sql, engine)
    logger.info(f"Extracted {len(df)} rows from Postgres.")
    return df
