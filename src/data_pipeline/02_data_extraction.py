import os
import zipfile
import hashlib
import shutil
from scipy.io import loadmat  # For .mat files


def calculate_file_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()



def extract_files_from_zip(download_folder, destination_folder, file_extensions):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    zip_files = [f for f in os.listdir(download_folder) if f.endswith('.zip')]
    if not zip_files:
        print(f"No .zip files found in {download_folder}.")
        return

    print(f"Found {len(zip_files)} .zip file(s) in {download_folder}.")

    for zip_file in zip_files:
        zip_file_path = os.path.join(download_folder, zip_file)
        print(f"\nProcessing {zip_file}...")

        try:
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                extracted_files = [
                    file for file in zip_ref.namelist() if any(file.endswith(ext) for ext in file_extensions)
                ]
                if not extracted_files:
                    print(f"No matching files found in {zip_file}. Skipping.")
                else:
                    for file in extracted_files:
                        extracted_file_path = os.path.join(destination_folder, file)
                        if not os.path.exists(extracted_file_path):
                            zip_ref.extract(file, destination_folder)
                            print(f"Extracted {file} to {destination_folder}.")
                        else:
                            temp_path = os.path.join(destination_folder, f"temp_{file}")
                            zip_ref.extract(file, destination_folder)
                            extracted_hash = calculate_file_hash(temp_path)
                            existing_hash = calculate_file_hash(extracted_file_path)
                            if extracted_hash == existing_hash:
                                os.remove(temp_path)
                                print(f"File {file} already exists with the same content. Skipping.")
                            else:
                                new_name = f"{os.path.splitext(file)[0]}_duplicate{os.path.splitext(file)[1]}"
                                new_path = os.path.join(destination_folder, new_name)
                                os.rename(temp_path, new_path)
                                print(f"Renamed {file} to {new_name} due to content mismatch.")
        except zipfile.BadZipFile:
            print(f"Error: {zip_file} is not a valid zip file. Skipping.")
        except Exception as e:
            print(f"An error occurred while processing {zip_file}: {e}")
        else:
            os.remove(zip_file_path)
            print(f"Deleted {zip_file_path} after successful extraction.")

    print("\nProcessing complete for all .zip files.")


def validate_mat_file(file_path):
    try:
        loadmat(file_path)
        return True
    except Exception:
        return False


def move_valid_files(source_folder, destination_folder, file_extensions):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for root, _, files in os.walk(source_folder):
        for file in files:
            if any(file.endswith(ext) for ext in file_extensions):
                source_file_path = os.path.join(root, file)
                if file.endswith('.mat') and not validate_mat_file(source_file_path):
                    print(f"Skipping invalid .mat file: {file}")
                    continue
                destination_file_path = os.path.join(destination_folder, file)
                if not os.path.exists(destination_file_path):
                    shutil.move(source_file_path, destination_file_path)
                    print(f"Moved {file} to {destination_folder}.")
                else:
                    print(f"File {file} already exists in {destination_folder}. Skipping.")


if __name__ == "__main__":
    download_folder = os.path.expanduser("~/Downloads")
    destination_folder = "/home/abdullahalazmi/Downloads/predictive_maintenance/data/raw"

    file_extensions = ['.csv', '.txt', '.mat']

    extract_files_from_zip(download_folder, destination_folder, file_extensions)
    move_valid_files(destination_folder, destination_folder, file_extensions)
