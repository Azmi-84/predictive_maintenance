import seaborn as sns
import matplotlib.pyplot as plt
import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def percentage_of_machines_by_type(df, ax):
    try:
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

def product_id_graph(df, ax):
    try:
        if 'Product ID' in df.columns:
            df['Product ID'] = df['Product ID'].str[1:].astype(float)
            sns.histplot(data=df, x='Product ID', bins=20, kde=True, ax=ax)
            ax.set_title("Distribution of Product IDs")
            ax.set_xlabel("Product ID")
            ax.set_ylabel("Count")
        else:
            logging.warning("Column 'Product ID' not found in the dataset.")
    except Exception as e:
        logging.error(f"Error creating product ID graph: {e}")

if __name__ == "__main__":
    setup_logging()