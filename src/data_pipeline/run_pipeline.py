import os
import hashlib
import logging
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from logger import setup_logging
from data_preprocessing import analyze_failure_relationship
from missing_data_imputation import target_anomalies, remove_rnf
from data_loading import load_data, num_to_float, rename_columns
from missing_data_analysis import global_percentage_of_removed_data, remove_inconsistent_failures
from data_visualization import percentage_of_machines_by_type, product_id_graph, numeric_features_graph

def setup_logging_directory(output_path):
    log_dir = os.path.join(output_path, "logs")
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir, exist_ok=True)
        except Exception as e:
            fallback_log_dir = os.path.expanduser("~/.logs/predictive_maintenance")
            try:
                os.makedirs(fallback_log_dir, exist_ok=True)
                log_dir = fallback_log_dir
            except Exception as fallback_error:
                raise RuntimeError(f"Failed to set up logging in both '{log_dir}' and fallback directory '{fallback_log_dir}'. "
                                   f"Errors: {e}, {fallback_error}")
    return os.path.join(log_dir, "pipeline.log")

log_file = setup_logging_directory("/desired/log/directory")
setup_logging(log_file=log_file)
logger = logging.getLogger(__name__)

def verify_file(file_path, expected_hash=None):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    if expected_hash:
        with open(file_path, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        if file_hash != expected_hash:
            raise ValueError("File hash does not match the expected hash!")
    return True

def setup_output_directory(output_path):
    os.makedirs(output_path, exist_ok=True)
    return output_path

def main(file_path, output_path, enable_visualizations=True):
    logger.info("Logging initialized.")

    try:
        verify_file(file_path)
        logger.info(f"File verified: {file_path}")
    except Exception as e:
        logger.error(f"File verification failed: {e}")
        return

    processed_data_dir = setup_output_directory(output_path)

    data = load_data(file_path)
    if data is None:
        logger.error("Failed to load data. Terminating pipeline.")
        return

    logger.info(f"Loaded data with {data.shape[0]} rows and {data.shape[1]} columns.")
    data = num_to_float(data)
    data = rename_columns(data)

    requiered_numeric_features = ["Air Temperature", "Process Temperature", "Rotational Speed", "Torque", "Tool Wear"]

    if enable_visualizations:
        try:
            fig, axes = plt.subplots(1, 2, figsize=(14, 7), constrained_layout=True)
            percentage_of_machines_by_type(data, axes[0])
            product_id_graph(data, axes[1])
            plt.tight_layout()
            plt.savefig(os.path.join(processed_data_dir, "visualization_summary.png"))
            plt.close()

            fig, ax = plt.subplots(figsize=(14, 7), constrained_layout=True)
            numeric_features_graph(data, requiered_features=requiered_numeric_features)
            plt.tight_layout()
            plt.savefig(os.path.join(processed_data_dir, "numeric_features.png"))
            plt.close()

            logger.info("Visualizations saved to the output directory.")
        except Exception as e:
            logger.warning(f"Failed to generate visualizations: {e}")

    data = target_anomalies(data)
    logger.info("Target anomalies identified and mapped.")

    data = remove_rnf(data)
    logger.info("Random failures removed from the dataset.")

    data = remove_inconsistent_failures(data)
    logger.info("Inconsistent failures removed from the dataset.")

    failure_analysis = analyze_failure_relationship(data)
    if failure_analysis:
        logger.info(f"Failure analysis: {failure_analysis}")

    removed_percentage = global_percentage_of_removed_data(data)
    logger.info(f"Percentage of rows with missing data: {removed_percentage:.3f}%.")

    output_file = os.path.join(processed_data_dir, "processed_data.csv")
    try:
        data.to_csv(output_file, index=False)
        logger.info(f"Processed data saved to '{output_file}'.")
    except Exception as e:
        logger.error(f"Failed to save processed data: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the predictive maintenance pipeline.")
    parser.add_argument(
        "--file",
        type=str,
        default="/home/abdullahalazmi/Downloads/predictive_maintenance/data/raw/kaggle_datasets/ai4i2020.csv",
        help="Path to the input CSV file. Default: preconfigured file path."
    )
    parser.add_argument(
        "--output",
        type=str,
        default="/home/abdullahalazmi/Downloads/predictive_maintenance/data/processed/",
        help="Path to the output directory. Default: preconfigured output path."
    )
    parser.add_argument(
        "--visualize",
        action="store_true",
        help="Enable real-time visualizations. Default is disabled."
    )
    parser.add_argument(
        "--hash",
        type=str,
        default=None,
        help="Optional SHA256 hash of the file for integrity verification."
    )
    args = parser.parse_args()

    main(file_path=args.file, output_path=args.output, enable_visualizations=args.visualize)
