import logging
import os
import yaml
import pandas as pd

def setup_logging(log_file=None, level=logging.INFO):
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file, mode='a'))
    
    logging.basicConfig(level=level, format=log_format, handlers=handlers)
    logging.info("Logging is configured.")

def load_config(config_path):
    if not os.path.exists(config_path):
        logging.error(f"Config file not found: {config_path}")
        return {}
    
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            logging.info(f"Config file loaded: {config_path}")
            return config
    except Exception as e:
        logging.error(f"Error loading config file: {e}")
        return {}

def validate_columns(df, required_columns):
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        logging.error(f"Missing required columns: {missing_columns}")
        return False
    return True

def save_dataframe(df, file_path):
    try:
        df.to_csv(file_path, index=False)
        logging.info(f"DataFrame saved to: {file_path}")
    except Exception as e:
        logging.error(f"Error saving DataFrame: {e}")

def filter_dataframe(df, column_name, condition):
    if column_name not in df.columns:
        logging.error(f"Column not found: {column_name}")
        return df
    
    try:
        filtered_df = df[condition(df[column_name])]
        logging.info(f"Filtered DataFrame based on column '{column_name}'. Rows remaining: {len(filtered_df)}")
        return filtered_df
    except Exception as e:
        logging.error(f"Error filtering DataFrame: {e}")
        return df

if __name__ == "__main__":
    setup_logging()