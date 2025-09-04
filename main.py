import logging
from config.settings import RAW_DATASET
from extract.postgres_extractor import extract_from_postgres
from extract.api_extractor import extract_from_api
from load.bigquery_loader import load_to_bigquery
from transform.user_posts_transform import transform_user_posts
from utils.validation import validate_dataframe
from utils.bq_utils import ensure_datasets, get_last_updated, update_last_updated

logger = logging.getLogger(__name__)

# ========== Main ==========
def main():
    try:
        ensure_datasets()

        # 1. Extract from Postgres incrementally
        last_updated = get_last_updated()
        df_users = extract_from_postgres(last_updated)
        if validate_dataframe(df_users, ["user_id", "email", "name", "updated_at"], "Postgres Users"):
            load_to_bigquery(df_users, RAW_DATASET, "users")
            max_ts = df_users["updated_at"].max()
            update_last_updated(max_ts)

        # 2. Extract from API (overwrite each run)
        df_posts = extract_from_api()
        if validate_dataframe(df_posts, ["userId", "id", "title", "body"], "API Posts"):
            load_to_bigquery(df_posts, RAW_DATASET, "posts", write_disposition="WRITE_TRUNCATE")

        # 3. Transform into staging
        transform_user_posts()

        logger.info("Pipeline completed successfully ✅")
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise

if __name__ == "__main__":
    main()
