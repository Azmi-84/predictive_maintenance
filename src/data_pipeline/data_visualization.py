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
            df['Product ID'] = df['Product ID'].str.extract(r'(\d+)').astype(float)  # Use raw string
            sns.histplot(data=df, x='Product ID', bins=20, kde=True, ax=ax)
            ax.set_title("Distribution of Product IDs")
            ax.set_xlabel("Product ID")
            ax.set_ylabel("Count")
        else:
            logging.warning("Column 'Product ID' not found in the dataset.")
    except Exception as e:
        logging.error(f"Error creating product ID graph: {e}")

def numeric_features_graph(df, ax):
    try:
        num_features = [feature for feature in df.columns if df[feature].dtype in ['int64', 'float64']]
        if not num_features:
            logging.warning("No numeric features found in the dataset.")
            return

        fig, axes = plt.subplots(nrows=2, ncols=(len(num_features) + 1) // 2, figsize=(18, 12))
        axes = axes.flatten()

        fig.suptitle("Numeric Features Histograms", fontsize=16)

        for i, feature in enumerate(num_features):
            sns.histplot(data=df, x=feature, bins=20, kde=True, ax=axes[i])
            axes[i].set_title(f"Histogram of {feature}")
            axes[i].set_xlabel(feature)
        
        fig, axes = plt.subplots(nrows=1, ncols=len(num_features), figsize=(18, 6))

        for j, feature in enumerate(num_features):
            sns.boxplot(data=df, y=feature, ax=axes[j])
            axes[j].set_title(f"Boxplot of {feature}")
            axes[j].set_ylabel(feature)

        plt.tight_layout()
    except Exception as e:
        logging.error(f"Error creating numeric features graph: {e}")

if __name__ == "__main__":
    setup_logging()