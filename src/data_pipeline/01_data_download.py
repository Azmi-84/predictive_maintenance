import os
from kaggle.api.kaggle_api_extended import KaggleApi
import hashlib

def hash_file(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def download_datasets(search_term, dest_folder, sort_by="hottest", page_limit=5):
    api = KaggleApi()
    api.authenticate()
    
    os.makedirs(dest_folder, exist_ok=True)

    for page in range(1, page_limit + 1):
        print(f"Fetching page {page} for datasets...")
        try:
            datasets = api.dataset_list(search=search_term, sort_by=sort_by, page=page)
            if not datasets:
                print("No datasets found.")
                break
            
            for dataset in datasets:
                dataset_ref = dataset.ref  # The reference string for the dataset
                dataset_name = dataset_ref.split("/")[-1]
                dataset_folder = os.path.join(dest_folder, dataset_name)

                if os.path.exists(dataset_folder):
                    print(f"Dataset '{dataset_name}' already downloaded, skipping...")
                    continue

                print(f"Downloading dataset: {dataset_name}...")
                try:
                    api.dataset_download_files(dataset_ref, path=dest_folder, unzip=True)
                    print(f"Successfully downloaded and extracted '{dataset_name}'.")
                except Exception as e:
                    print(f"Error downloading '{dataset_name}': {str(e)}")
        except Exception as e:
            print(f"Error fetching datasets on page {page}: {str(e)}")
            break

if __name__ == "__main__":
    SEARCH_TERM = "Predictive Maintenance Dataset"
    DESTINATION_FOLDER = "data/raw/./kaggle_datasets"
    SORT_ORDER = "hottest"  # Options: newest, oldest, hottest, etc.
    PAGE_LIMIT = 6

    download_datasets(SEARCH_TERM, DESTINATION_FOLDER, SORT_ORDER, PAGE_LIMIT)
