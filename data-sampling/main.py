from typing import Any

import os
import pandas as pd
import numpy as np
import time
import logging
import sampling
import statistical_tests
import HTML_report

INPUT_FILE_PATH = 'data/202206-202305-cleaned-cyclistic.csv'
OUTPUT_FILE_PATH = 'output/202206-202305_sample_cyclistic.csv'
LOG_FILE = 'output/log.txt'

# Define the sample size and stratify variables
sample_size = 100000
stratify_variables = ['month']

def create_output_folders():
    # Create a folder for output if it doesn't exist
    if not os.path.exists('output'):
        os.makedirs('output')

    # Create a folder for plots if it doesn't exist
    if not os.path.exists('output/plots'):
        os.makedirs('output/plots')

def read_data(file_path):
    logging.info("Start reading data")
    try:
        data = pd.read_csv(file_path)
        logging.info("Data is ready")
        return data
    except FileNotFoundError:
        logging.error("File not found: {}".format(file_path))
    except pd.errors.EmptyDataError:
        logging.error("Empty data file: {}".format(file_path))
    except pd.errors.ParserError:
        logging.error("Parsing error: {}".format(file_path))

    return None

def generate_html_report(full_data, sample_data, sizes, numeric_columns, categorical_columns, mean_df, std_df, corr_full_data_df, corr_sample_data_df, ks_results_df, chi2_results_df):
    HTML_report.run_report(full_data, sample_data, numeric_columns, categorical_columns, sizes,
                           mean_df, std_df, corr_full_data_df, corr_sample_data_df, ks_results_df, chi2_results_df)

def setup_logging():
    log_file = LOG_FILE
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

def clean_log_file():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as file:
            file.write('')  # Write an empty string to clear the file


def main():
    start_time = time.time()
    clean_log_file()

    create_output_folders()
    setup_logging()

    full_data = read_data(INPUT_FILE_PATH)
    if full_data is None:
        logging.error("Failed to read data. Exiting...")
        return


    weights = sampling.calculate_weights(full_data, stratify_variables)
    sample_data = sampling.stratified_sampling(full_data, stratify_variables, sample_size, weights)

    if sample_data is None:
        logging.error("Failed to perform stratified sampling. Exiting...")
        return

    logging.info("Running statistical tests started")
    sizes = statistical_tests.data_sizes(full_data, sample_data)
    numeric_columns = full_data.select_dtypes(include=[np.number]).columns
    categorical_columns = ['user_type', 'bike_type', 'name_day_of_week']

    mean_df, std_df, corr_full_data_df, corr_sample_data_df = statistical_tests.compare_statistics(
        full_data, sample_data, numeric_columns)
    logging.info("Main statistics are calculated")
    ks_results_df = statistical_tests.kolmogorov_smirnov_test(full_data, sample_data, numeric_columns)
    logging.info("Kolmogorov-Smirnov test is calculated")
    chi2_results_df = statistical_tests.chi_square_test(full_data, sample_data, categorical_columns)
    logging.info("Chi-square test is calculated")

    generate_html_report(full_data, sample_data, sizes, numeric_columns, categorical_columns, mean_df, std_df,
                         corr_full_data_df, corr_sample_data_df, ks_results_df, chi2_results_df)

    sample_data.to_csv(OUTPUT_FILE_PATH, index=False)

    end_time = time.time()
    execution_time = end_time - start_time

    logging.info("Execution time: {} seconds".format(execution_time))

if __name__ == "__main__":
    main()


