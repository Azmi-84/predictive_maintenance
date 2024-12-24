import os

from kaggle.api.kaggle_api_extended import KaggleApi

api = KaggleApi()
api.authenticate()

page = 1
while True:
    datasets = api.dataset_list(search="Predictive Maintenance Dataset", page=page)
    if not datasets:
        break
    print(f"Page: {page}")
    for idx, dataset in enumerate(datasets):
        print(f"Title: {dataset.title}")
        print(f"Dataset ID: {dataset.ref}")
        print(f"Dataset Tags: {dataset.tags}")
        print(f"URL: https://www.kaggle.com/datasets/{dataset.ref}")
        print("-" * 50)
        print(f"\nDetails of dataset {idx + 1}:")
        ds_vars = vars(dataset)
        for var, value in ds_vars.items():
            print(f"{var} = {value}")
        print("-" * 80)
    page += 1
