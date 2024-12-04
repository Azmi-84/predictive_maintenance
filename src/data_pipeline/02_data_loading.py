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
    # df.info()

    n = df.shape[0]
    unique_products = df['Product ID'].nunique() if 'Product ID' in df.columns else 0
    has_duplicates = unique_products != n
    logging.info(f"Check for duplicate Product IDs: {'Found duplicates' if has_duplicates else 'No duplicates'}")
    # logging.info(f"Original columns: {df.columns.tolist()}")

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
    
    # logging.info(f"Updated dtypes: {df.dtypes}")
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

def target_anomalies(df):
    failure_columns = ['TWF', 'HDF', 'PWF', 'OSF', 'RNF']
    if not all(col in df.columns for col in failure_columns):
        missing_cols = [col for col in failure_columns if col not in df.columns]
        logging.error(f"Missing failure columns: {missing_cols}")
        return df

    try:
        failure_mapping = {
            'TWF': 'Tool Wear Failure',
            'HDF': 'Heat Dissipation Failure',
            'PWF': 'Power Failure',
            'OSF': 'Overstrain Failure',
            'RNF': 'Random Failure'
        }

        df['Failure Type'] = df[failure_columns].idxmax(axis=1).map(failure_mapping)
        logging.info(f"Derived 'Failure Type' column:\n{df['Failure Type'].value_counts()}")

        idx_RNF = df.loc[df['Failure Type'] == 'Random Failure'].index
        logging.info(f"Indexes with Random Failures: {idx_RNF.tolist()}")
        
        features = [col for col in df.columns if df[col].dtype == 'float64' or col == 'Type']
        logging.info(f"Relevant features: {features}")

    except Exception as e:
        logging.error(f"Error processing target anomalies: {e}")

    return df

def remove__rnf(df):
    try:
        idx_RNF = df.loc[df['Failure Type'] == 'Random Failure'].index
        df.drop(idx_RNF, inplace=True)
        logging.info(f"Removed Random Failures: {idx_RNF.tolist()}")
    except Exception as e:
        logging.error(f"Error removing Random Failures: {e}")
    return df


def analyze_failure_relationship(df):
    """
    Analyzing and counting the occurrences of specific failure conditions,
    logging the row numbers for each condition.
    """
    try:
        required_columns = ['RNF', 'Machine failure']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Missing required columns: {required_columns}")

        conditions = {
            "Random=1, Machine=0": {"count": 0, "rows": []},
        }

        for index, (random_failure, machine_failure) in enumerate(zip(df['RNF'], df['Machine failure']), start=1):
            if random_failure == 1 and machine_failure == 0:
                condition = "Random=1, Machine=0"
            else:
                continue

            conditions[condition]["count"] += 1
            conditions[condition]["rows"].append(index)

        for condition, data in conditions.items():
            logging.info(f"{condition}: {data['count']} occurrences. Rows: {data['rows']}")

        return conditions

    except Exception as e:
        logging.error(f"Error analyzing and counting failures: {e}")
        return None

if __name__ == "__main__":
    file_path = "/home/abdullahalazmi/Downloads/predictive_maintenance/data/raw/kaggle_datasets/ai4i2020.csv"

    if os.path.exists(file_path):
        data = load_data(file_path)
        if data is not None:
            data = num_to_float(data)
            data = rename_columns(data)
            
            # fig, axes = plt.subplots(1, 2, figsize=(14, 7))
            # data = percentage_of_machines_by_type(data, axes[0])
            # data = product_id_graph(data, axes[1])
            
            # plt.tight_layout()
            # plt.show()

            # data = target_anomalies(data)
            # data = remove__rnf(data)

            data = analyze_failure_relationship(data)
    else:
        logging.error(f"File not found: {file_path}")
