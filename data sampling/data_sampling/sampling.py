import matplotlib.pyplot as plt
import os
import base64
import pandas as pd
import numpy as np
import time
from scipy.stats import ks_2samp
from scipy.stats import chi2_contingency
import pandas_profiling



# Calculate weights for each data point based on the stratification variables
def calculate_weights(data, feature_names):
    counts = data[feature_names].apply(pd.value_counts)
    data_weights = np.zeros(len(data))
    for feature in feature_names:
        variable_counts = counts[feature].reindex(data[feature])
        data_weights += 1 / variable_counts.values
    return data_weights

def stratified_sampling(data,stratify_s_variables,sample_size,weights):
    # Apply stratified sampling
    s_sample_data = pd.DataFrame()
    for group_name, group_data in data.groupby(stratify_s_variables):
        # Calculate the number of rows to sample from this group
        group_size = len(group_data)
        sample_group_size = int(round((group_size / len(data)) * sample_size))

        # Sample from the group using the calculated weights
        sampled_indices = np.random.choice(
            group_data.index, size=sample_group_size, replace=False,
            p=weights[group_data.index] / np.sum(weights[group_data.index])
        )
        sampled_group_data = group_data.loc[sampled_indices]

        # Append the sampled data to the sample_data DataFrame
        s_sample_data = pd.concat([s_sample_data, sampled_group_data])

    # Reset the index of the sample data
    s_sample_data.reset_index(drop=True, inplace=True)
    return s_sample_data
