import os
import argparse
import logging
from logger import setup_logging
from data_loading import load_data, num_to_float, rename_columns
from missing_data_analysis import global_percentage_of_removed_data, remove_inconsistent_failures
from missing_data_imputation import target_anomalies, remove_rnf
from data_preprocessing import analyze_failure_relationship
from visualization import percentage_of_machines_by_type, product_id_graph
import matplotlib.pyplot as plt

def main(file_path, output_path):
    setup_logging(log_file=os.path.join(output_path, 'pipeline.log'))
    logger = logging.getLogger(__name__)

    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return

    data = load_data(file_path)
    if data is None:
        logger.error("Failed to load data.")
        return

    data = num_to_float(data)
    data = rename_columns(data)

    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    percentage_of_machines_by_type(data, axes[0])
    product_id_graph(data, axes[1])
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, "visualizations.png"))
    logger.info("Visualizations saved as 'visualizations.png'.")

    data = target_anomalies(data)
    data = remove_rnf(data)
    data = remove_inconsistent_failures(data)

    failure_analysis = analyze_failure_relationship(data)
    removed_percentage = global_percentage_of_removed_data(data)

    output_file = os.path.join(output_path, "processed_data.csv")
    data.to_csv(output_file, index=False)
    logger.info(f"Processed data saved to {output_file}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        type=str,
        required=True,
        help="Path to the input CSV file"
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Path to the output directory"
    )
    args = parser.parse_args()

    main(args.file, args.output)