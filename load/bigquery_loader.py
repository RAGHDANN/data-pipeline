import pandas as pd
import logging
from google.cloud import bigquery
from config.settings import bq_client, GCP_PROJECT_ID

logger = logging.getLogger(__name__)

def load_to_bigquery(df, dataset, table, write_disposition="WRITE_APPEND"):
    """Load DataFrame into BigQuery"""
    table_ref = f"{GCP_PROJECT_ID}.{dataset}.{table}"
    job_config = bigquery.LoadJobConfig(
        write_disposition=write_disposition,
        autodetect=True,
    )
    job = bq_client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()
    logger.info(f"Loaded {len(df)} rows into {table_ref}.")
