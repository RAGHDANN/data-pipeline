import logging

logger = logging.getLogger(__name__)

def validate_dataframe(df, required_columns, source_name):
    """Basic data validation for DataFrames"""
    if df.empty:
        logger.warning(f"{source_name}: DataFrame is empty!")
        return False
    
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        logger.error(f"{source_name}: Missing columns {missing}")
        return False
    
    logger.info(f"{source_name}: Validation passed ✅")
    return True
