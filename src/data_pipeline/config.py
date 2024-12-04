COLUMNS = {
    "rename_map": {
        'Air temperature [K]': 'Air temperature',
        'Process temperature [K]': 'Process temperature',
        'Rotational speed [rpm]': 'Rotational speed',
        'Torque [Nm]': 'Torque',
        'Tool wear [min]': 'Tool wear'
    },
    "failure_columns": ['TWF', 'HDF', 'PWF', 'OSF', 'RNF']
}

DEFAULT_CSV_PATH = "/home/abdullahalazmi/Downloads/predictive_maintenance/data/raw/kaggle_datasets/ai4i2020.csv"
PROCESSED_CSV_PATH = "/home/abdullahalazmi/Downloads/predictive_maintenance/data/processed/processed_data.csv"
VISUALIZATION_PATH = "/home/abdullahalazmi/Downloads/predictive_maintenance/data/processed/visualizations.png"