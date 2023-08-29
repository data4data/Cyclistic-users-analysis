import matplotlib.pyplot as plt
import os
import base64
import pandas as pd
import numpy as np
from scipy.stats import ks_2samp
from scipy.stats import chi2_contingency
import pandas_profiling


def data_sizes(full_data, sample_data):
    size_data = {
        'Full Data': [full_data.shape[0], full_data.shape[1]],
        'Sample Data': [sample_data.shape[0], sample_data.shape[1]]
    }
    size_df = pd.DataFrame(size_data, index=['Rows', 'Columns']).T
    return size_df


def compare_statistics(full_data, sample_data, numeric_columns):
    # Create DataFrames
    mean_df = pd.DataFrame({'Full Data': full_data[numeric_columns].mean(), 'Sample Data': sample_data[numeric_columns].mean()})
    std_df = pd.DataFrame({'Full Data': full_data[numeric_columns].std(), 'Sample Data': sample_data[numeric_columns].std()})
    corr_full_data_df = pd.DataFrame(full_data[numeric_columns].corr(), columns=numeric_columns, index=numeric_columns)
    corr_sample_data_df = pd.DataFrame(sample_data[numeric_columns].corr(), columns=numeric_columns, index=numeric_columns)

    return mean_df, std_df, corr_full_data_df, corr_sample_data_df


def kolmogorov_smirnov_test(data, sampledata, numb_columns):
    ks_results = {}
    for variable in numb_columns:
        ks_stat, p_value = ks_2samp(data[variable], sampledata[variable])
        ks_results[variable] = {'KS statistic': ks_stat, 'p-value': p_value}

    # Create DataFrame from ks_results dictionary
    ks_results_df = pd.DataFrame(ks_results).T

    return ks_results_df


def chi_square_test(data, sampledata, cat_columns):
    chi2_results = {}
    for column in cat_columns:
        # Create a contingency table
        contingency_table = pd.crosstab(data[column], sampledata[column])

        # Perform chi-square test
        chi2_stat, p_value, _, _ = chi2_contingency(contingency_table)

        # Store the results in the chi2_results dictionary
        chi2_results[column] = {'Chi-square statistic': chi2_stat, 'p-value': p_value}

    # Create DataFrame from chi2_results dictionary
    chi2_results_df = pd.DataFrame(chi2_results).T

    return chi2_results_df