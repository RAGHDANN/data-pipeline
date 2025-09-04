import logging
from google.cloud import bigquery
from config.settings import bq_client, GCP_PROJECT_ID, RAW_DATASET, STAGING_DATASET

logger = logging.getLogger(__name__)

def ensure_datasets():
    """Ensure that required BigQuery datasets exist"""
    for dataset in [RAW_DATASET, STAGING_DATASET]:
        dataset_ref = bigquery.Dataset(f"{GCP_PROJECT_ID}.{dataset}")
        try:
            bq_client.get_dataset(dataset_ref)
            logger.info(f"Dataset {dataset} already exists.")
        except Exception:
            bq_client.create_dataset(dataset_ref)
            logger.info(f"Created dataset {dataset}.")

def validate_table_in_bq(dataset, table):
    """Check row count in a BigQuery table"""
    query = f"SELECT COUNT(*) as cnt FROM `{GCP_PROJECT_ID}.{dataset}.{table}`"
    results = bq_client.query(query).result()
    for row in results:
        logger.info(f"Table {dataset}.{table} has {row.cnt} rows.")

def get_last_updated():
    """Retrieve last updated timestamp from pipeline_state"""
    query = f"""
    CREATE TABLE IF NOT EXISTS `{GCP_PROJECT_ID}.{RAW_DATASET}.pipeline_state` (
        table_name STRING,
        last_updated_at TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
    )
    """
    bq_client.query(query).result()

    query = f"""
    SELECT last_updated_at
    FROM `{GCP_PROJECT_ID}.{RAW_DATASET}.pipeline_state`
    WHERE table_name = 'users'
    ORDER BY created_at DESC
    LIMIT 1
    """
    results = bq_client.query(query).result()
    for row in results:
        return row.last_updated_at
    return None

def update_last_updated(timestamp):
    """Update pipeline_state with new timestamp"""
    query = f"""
    INSERT INTO `{GCP_PROJECT_ID}.{RAW_DATASET}.pipeline_state` (table_name, last_updated_at)
    VALUES ('users', '{timestamp}')
    """
    bq_client.query(query).result()
    logger.info("Updated pipeline_state.")
