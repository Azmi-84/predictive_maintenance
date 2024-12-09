import seaborn as sns
import matplotlib.pyplot as plt
import logging

# Initialize logging
def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Visualize the percentage of machines by type
def percentage_of_machines_by_type(df, ax):
    try:
        if 'Type' in df.columns:
            machine_type_counts = df['Type'].value_counts(normalize=True) * 100
            logging.info(f"Percentage of machines by type:\n{machine_type_counts}")
            
            sns.barplot(
                x=machine_type_counts.index,
                y=machine_type_counts.values,
                ax=ax,
                palette=sns.color_palette("pastel")  # Pastel color palette for clear visuals
            )
            
            ax.set_title("Percentage of Machines by Type")
            ax.set_xlabel("Machine Type")
            ax.set_ylabel("Percentage")
        else:
            logging.warning("Column 'Type' not found in the dataset.")
    except Exception as e:
        logging.error(f"Error calculating percentage of machines by type: {e}")

# Plot a histogram of product IDs
def product_id_graph(df, ax):
    try:
        if 'Product ID' in df.columns:
            # Extract numeric parts of 'Product ID'
            df['Product ID'] = df['Product ID'].str.extract(r'(\d+)').astype(float)
            
            sns.histplot(
                data=df,
                x='Product ID',
                bins=20,
                kde=True,
                ax=ax,
                color=sns.color_palette("coolwarm", 10)[3]  # Cool-warm palette for distinction
            )
            
            ax.set_title("Distribution of Product IDs")
            ax.set_xlabel("Product ID")
            ax.set_ylabel("Count")
        else:
            logging.warning("Column 'Product ID' not found in the dataset.")
    except Exception as e:
        logging.error(f"Error creating product ID graph: {e}")

# Create histograms and boxplots for numeric features
def numeric_features_graph(df, required_features=None):
    try:
        # Select numeric features
        num_features = [feature for feature in df.columns if df[feature].dtype in ['int64', 'float64']]
        if required_features:
            num_features = [feature for feature in num_features if feature in required_features]
        if not num_features:
            logging.warning("No numeric features found in the dataset.")
            return

        # Create histograms
        ncols = 2  # Number of columns for subplots
        nrows = (len(num_features) + ncols - 1) // ncols  # Calculate rows based on features
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols * 6, nrows * 5), constrained_layout=True)
        axes = axes.flatten()

        for i, feature in enumerate(num_features):
            sns.histplot(
                data=df,
                x=feature,
                bins=20,
                kde=True,
                ax=axes[i],
                color=sns.color_palette("Set2")[i % len(sns.color_palette("Set2"))]  # Rotate through Set2 palette
            )
            axes[i].set_title(f"{feature} - Histogram")
            axes[i].set_xlabel(feature)
            axes[i].set_ylabel("Frequency")

        # Remove unused subplots
        for j in range(i + 1, len(axes)):
            fig.delaxes(axes[j])

        # Boxplots for numeric features
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols * 6, nrows * 5), constrained_layout=True)
        axes = axes.flatten()

        for i, feature in enumerate(num_features):
            sns.boxplot(
                data=df,
                y=feature,
                ax=axes[i],
                color=sns.color_palette("Set3")[i % len(sns.color_palette("Set3"))]  # Rotate through Set3 palette
            )
            axes[i].set_title(f"{feature} - Boxplot")
            axes[i].set_ylabel(feature)

        # Remove unused subplots
        for j in range(i + 1, len(axes)):
            fig.delaxes(axes[j])

    except Exception as e:
        logging.error(f"Error creating numeric features graph: {e}")

if __name__ == "__main__":
    setup_logging()
