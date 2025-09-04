import pandas as pd
import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def extract_from_api():
    """Dummy API extractor using JSONPlaceholder"""
    url = "https://jsonplaceholder.typicode.com/posts"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    df = pd.json_normalize(data)
    df["extracted_at"] = datetime.utcnow()
    logger.info(f"Extracted {len(df)} rows from API.")
    return df
