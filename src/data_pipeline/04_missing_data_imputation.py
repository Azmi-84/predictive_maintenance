import os
import pandas as pd
from scipy.io import loadmat


def check_duplicate_headers(file_path, headers_output_path):
    """
    Checks if a file's header is already in the headers summary file.

    Parameters:
        file_path (str): Path to the file.
        headers_output_path (str): Path to the headers summary file.

    Returns:
        bool: True if the header is a duplicate, False otherwise.
    """
    extension = os.path.splitext(file_path)[1].lower()

    if extension in [".csv", ".txt"]:
        df = pd.read_csv(file_path, delimiter='\t' if extension == ".txt" else ',')
        header = ", ".join(df.columns)
    elif extension == ".mat":
        mat_data = loadmat(file_path)
        data_key = next((key for key in mat_data.keys() if not key.startswith('__')), None)
        if data_key:
            header = ", ".join([f"Column {i}" for i in range(mat_data[data_key].shape[1])])
        else:
            return True  # No valid header

    if os.path.exists(headers_output_path):
        with open(headers_output_path, "r") as f:
            content = f.read()
            if header in content:
                return True
    return False


def process_file_in_chunks(file_path, chunk_size=100000):
    """
    Processes a file in chunks to handle large datasets.

    Parameters:
        file_path (str): Path to the file.
        chunk_size (int): Number of rows per chunk.

    Returns:
        DataFrame: Combined DataFrame of the file (if feasible to load in chunks).
    """
    try:
        extension = os.path.splitext(file_path)[1].lower()

        if extension in [".csv", ".txt"]:
            delimiter = '\t' if extension == ".txt" else ','
            chunk_list = []

            for chunk in pd.read_csv(file_path, chunksize=chunk_size, delimiter=delimiter):
                chunk_list.append(chunk)

            return pd.concat(chunk_list, ignore_index=True)
        elif extension == ".mat":
            mat_data = loadmat(file_path)
            data_key = next((key for key in mat_data.keys() if not key.startswith('__')), None)
            if data_key:
                return pd.DataFrame(mat_data[data_key])
        else:
            print(f"Unsupported file format: {file_path}")
            return None
    except Exception as e:
        print(f"An error occurred while processing {file_path} in chunks: {e}")
        return None


def highlight_missing_rows(df, file_path, output_folder):
    """
    Highlights rows with missing values and saves them in a separate file.

    Parameters:
        df (DataFrame): The DataFrame of the file.
        file_path (str): Path to the file.
        output_folder (str): Path to save filtered rows with missing values.

    Returns:
        None
    """
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        missing_rows = df[df.isnull().any(axis=1)]
        if not missing_rows.empty:
            output_file = os.path.join(output_folder, f"missing_rows_{os.path.basename(file_path)}")
            missing_rows.to_csv(output_file, index=False)
            print(f"Missing rows saved to {output_file}.")
        else:
            print(f"No missing rows in {file_path}.")
    except Exception as e:
        print(f"An error occurred while saving missing rows for {file_path}: {e}")


def main():
    """
    Main function to handle large files, check headers, and save rows with missing values.
    """
    folder_path = "/home/abdullahalazmi/Downloads/predictive_maintenance/data/raw"
    headers_output_path = "/home/abdullahalazmi/Downloads/predictive_maintenance/headers_summary.txt"
    missing_rows_folder = "/home/abdullahalazmi/Downloads/predictive_maintenance/missing_rows"

    if not os.path.exists(folder_path):
        print(f"Error: The folder {folder_path} does not exist.")
        return

    # Clear or create the headers summary file
    with open(headers_output_path, "w") as f:
        f.write("Headers Summary for All Files\n")
        f.write("=" * 50 + "\n\n")

    # Iterate through all files in the folder
    total_missing_values = 0
    file_count = 0

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        # Check if it's a file (skip subdirectories)
        if os.path.isfile(file_path):
            print(f"Analyzing file: {file_name}")

            # Check for duplicate headers
            if check_duplicate_headers(file_path, headers_output_path):
                print(f"Skipping file {file_name} due to duplicate headers.")
                continue

            # Process file in chunks to handle large data
            df = process_file_in_chunks(file_path)
            if df is None:
                continue

            # Check for missing values
            missing_values = df.isnull().sum().sum()
            if missing_values > 0:
                total_missing_values += missing_values
                print(f"⚠️ Found {missing_values} missing values in {file_name}.")

                # Highlight missing rows and save them
                highlight_missing_rows(df, file_path, missing_rows_folder)

            # Save headers
            with open(headers_output_path, "a") as f:
                f.write(f"Headers for {file_name}:\n")
                f.write(", ".join(df.columns) + "\n\n")
            file_count += 1

    print(f"\nProcessed {file_count} file(s).")
    print(f"Total missing values across all files: {total_missing_values}")
    print(f"Filtered rows with missing values saved in: {missing_rows_folder}")


if __name__ == "__main__":
    main()
