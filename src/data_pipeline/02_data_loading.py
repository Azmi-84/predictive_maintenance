import os
import pandas as pd
import logging
import seaborn as sns
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        logging.info("File loaded successfully.")
    except Exception as e:
        logging.error(f"Error loading file: {e}")
        return None

    logging.info('Initial data overview:')
    df.info()

    n = df.shape[0]
    unique_products = df['Product ID'].nunique() if 'Product ID' in df.columns else 0
    has_duplicates = unique_products != n
    logging.info(f"Check for duplicate Product IDs: {'Found duplicates' if has_duplicates else 'No duplicates'}")
    logging.info(f"Original columns: {df.columns.tolist()}")

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
    
    logging.info(f"Updated dtypes: {df.dtypes}")
    return df

def rename_columns(df):
    try:
        df.rename(mapper={'Air temperature [K]': 'Air temperature',
                          'Process temperature [K]': 'Process temperature',
                          'Rotational speed [rpm]': 'Rotational speed',
                          'Torque [Nm]': 'Torque',
                          'Tool wear [min]': 'Tool wear'}, 
                  axis=1, inplace=True)
        logging.info(f"New columns: {df.columns.tolist()}")
    except Exception as e:
        logging.error(f"Error renaming columns: {e}")
    return df

def percentage_of_machines_by_type(df, ax):
    try:
        if 'Product ID' in df.columns:
            df['Product ID'] = df['Product ID'].astype(str)
            df['Product ID'] = df['Product ID'].apply(lambda x: x[1:])
            df['Product ID'] = pd.to_numeric(df['Product ID'], errors='coerce')
        
        if 'Type' in df.columns:
            machine_type_counts = df['Type'].value_counts(normalize=True) * 100
            logging.info(f"Percentage of machines by type:\n{machine_type_counts}")
            sns.barplot(x=machine_type_counts.index, y=machine_type_counts.values, ax=ax)
            ax.set_title("Percentage of Machines by Type")
            ax.set_xlabel("Machine Type")
            ax.set_ylabel("Percentage")
        else:
            logging.warning("Column 'Type' not found in the dataset.")
    except Exception as e:
        logging.error(f"Error calculating percentage of machines by type: {e}")
    return df

def product_id_graph(df, ax):
    try:
        if 'Product ID' in df.columns:
            df['Product ID'] = df['Product ID'].astype(str)
            df['Product ID'] = df['Product ID'].apply(lambda x: x[1:])
            df['Product ID'] = pd.to_numeric(df['Product ID'], errors='coerce')
        
        sns.histplot(data=df, x='Product ID', bins=20, kde=True, ax=ax)
        ax.set_title("Distribution of Product IDs")
        ax.set_xlabel("Product ID")
        ax.set_ylabel("Count")
    except Exception as e:
        logging.error(f"Error creating product ID graph: {e}")
    return df

if __name__ == "__main__":
    file_path = "/home/abdullahalazmi/Downloads/predictive_maintenance/data/raw/kaggle_datasets/ai4i2020.csv"

    if os.path.exists(file_path):
        data = load_data(file_path)
        if data is not None:
            data = num_to_float(data)
            data = rename_columns(data)
            
            fig, axes = plt.subplots(1, 2, figsize=(14, 7))
            data = percentage_of_machines_by_type(data, axes[0])
            data = product_id_graph(data, axes[1])
            
            plt.tight_layout()
            plt.show()
    else:
        logging.error(f"File not found: {file_path}")
