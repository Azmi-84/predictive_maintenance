import pandas as pd
import logging
from config import COLUMNS

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        df.fillna(value=0, inplace=True)
        logging.info("File loaded successfully.")
    except Exception as e:
        logging.error(f"Error loading file: {e}")
        return None
    return df

def num_to_float(df):
    for col in ['Tool wear [min]', 'Rotational speed [rpm]']:
        if col in df.columns:
            try:
                df[col] = df[col].astype('float64')
            except Exception as e:
                logging.error(f"Error converting column {col}: {e}")
        else:
            logging.warning(f"Column {col} not found in the dataset.")
    return df

def rename_columns(df):
    try:
        df.rename(columns=COLUMNS["rename_map"], inplace=True)
        logging.info(f"Renamed columns: {df.columns.tolist()}")
    except Exception as e:
        logging.error(f"Error renaming columns: {e}")
    return df

if __name__ == "__main__":
    setup_logging()