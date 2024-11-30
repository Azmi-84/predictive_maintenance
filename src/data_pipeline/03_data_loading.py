import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from scipy.io import loadmat
from extract_and_move import extract_csv_from_zip


def load_data(file_path):
    """
    Loads data from a specified file (.csv, .txt, or .mat).

    Args:
        file_path (str): The full path to the file.

    Returns:
        pd.DataFrame: The loaded data, or None if an error occurred.
    """
    try:
        if not os.path.exists(file_path):
            print(f"Error: The file {file_path} does not exist.")
            return None

        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".csv":
            data = pd.read_csv(file_path)
        elif extension == ".txt":
            data = pd.read_csv(file_path, delimiter='\t')  # Assuming tab-delimited text
        elif extension == ".mat":
            mat_data = loadmat(file_path)
            data_key = next((key for key in mat_data.keys() if not key.startswith('__')), None)
            if data_key:
                data = pd.DataFrame(mat_data[data_key])
            else:
                print(f"Error: No valid data key found in {file_path}.")
                return None
        else:
            print(f"Error: Unsupported file format for {file_path}.")
            return None

        if data.empty:
            print(f"Error: The file {file_path} is empty.")
            return None

        print(f"\n✅ Data loaded successfully from {file_path}.")
        print("First 5 rows of the data:")
        print(data.head())
        print("\n📊 Basic Statistics:")
        print(data.describe(include='all', percentiles=[0.25, 0.5, 0.75]).transpose())
        return data

    except Exception as e:
        print(f"An unexpected error occurred with file {file_path}: {e}")
    return None


def static_visualization(data, file_name):
    """
    Visualizes the numeric columns of the data using pairplot (static visualization).

    Args:
        data (pd.DataFrame): The dataset to visualize.
        file_name (str): The name of the file being visualized.
    """
    numeric_cols = data.select_dtypes(include=["number"])
    if numeric_cols.empty:
        print(f"Error: No numeric columns available for visualization in {file_name}.")
        return

    try:
        print(f"\n📈 Creating static visualization for {file_name}...")
        sns.pairplot(numeric_cols, diag_kind='kde', corner=True)
        plt.suptitle(f"Pairplot for {file_name}", y=1.02)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"An error occurred during static visualization of {file_name}: {e}")


def interactive_visualization(data, file_name):
    """
    Creates an interactive visualization for numeric columns using Plotly.

    Args:
        data (pd.DataFrame): The dataset to visualize.
        file_name (str): The name of the file being visualized.
    """
    numeric_cols = data.select_dtypes(include=["number"])
    if numeric_cols.empty:
        print(f"Error: No numeric columns available for interactive visualization in {file_name}.")
        return

    try:
        print(f"\n🌟 Creating interactive visualization for {file_name}...")
        fig = px.scatter_matrix(
            numeric_cols,
            dimensions=numeric_cols.columns,
            title=f"Interactive Scatter Matrix for {file_name}",
            labels={col: col.replace("_", " ").title() for col in numeric_cols.columns},
        )
        fig.update_traces(diagonal_visible=False)
        fig.show()
    except Exception as e:
        print(f"An error occurred during interactive visualization of {file_name}: {e}")


def process_folder(folder_path):
    """
    Iterates through all supported files in a folder, loads data, displays statistics,
    and visualizes the data both statically and interactively.

    Args:
        folder_path (str): The path to the folder containing the files.
    """
    if not os.path.exists(folder_path):
        print(f"Error: The folder {folder_path} does not exist.")
        return

    files = [f for f in os.listdir(folder_path) if f.endswith(('.csv', '.txt', '.mat'))]
    if not files:
        print(f"⚠️ No supported files found in folder {folder_path}.")
        return

    print(f"📂 Found {len(files)} file(s) in {folder_path}. Starting processing...\n")
    for idx, file_name in enumerate(files, start=1):
        file_path = os.path.join(folder_path, file_name)
        print(f"\n🔍 Processing file {idx}/{len(files)}: {file_name}")
        data = load_data(file_path)

        if data is not None:
            static_visualization(data, file_name)
            interactive_visualization(data, file_name)


def main():
    """
    Main function to orchestrate the workflow: extraction, data loading, and visualization.
    """
    # Define paths
    download_folder = os.path.expanduser("~/Downloads")  # Replace with your downloads folder path
    destination_folder = "/home/abdullahalazmi/Downloads/predictive_maintenance/data/raw"

    # Step 1: Extract and move files
    print("📦 Running extraction script...")
    extract_csv_from_zip(download_folder, destination_folder)

    # Step 2: Process all files in the destination folder
    print("\n🔄 Processing data files...")
    process_folder(destination_folder)


if __name__ == "__main__":
    main()
