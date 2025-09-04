import logging
from config.settings import bq_client, GCP_PROJECT_ID, STAGING_DATASET, RAW_DATASET
from utils.bq_utils import validate_table_in_bq

logger = logging.getLogger(__name__)

def transform_user_posts():
    """Join users (Postgres) with posts (API) into staging.user_posts"""
    query = f"""
    CREATE OR REPLACE TABLE `{GCP_PROJECT_ID}.{STAGING_DATASET}.user_posts` AS
    SELECT 
        u.user_id,
        u.email,
        u.name,
        u.created_at as user_created_at,
        p.userId as api_user_id,
        p.id as post_id,
        p.title as post_title,
        p.body as post_body,
        p.extracted_at
    FROM `{GCP_PROJECT_ID}.{RAW_DATASET}.users` u
    LEFT JOIN `{GCP_PROJECT_ID}.{RAW_DATASET}.posts` p
    ON u.user_id = p.userId
    WHERE u.user_id <= 10
    """
    bq_client.query(query).result()
    logger.info("Created staging.user_posts table.")
    validate_table_in_bq(STAGING_DATASET, "user_posts")
