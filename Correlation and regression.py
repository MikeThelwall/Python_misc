# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 19:55:15 2024

@author: Mike Thelwall
"""
import pandas as pd
from scipy.stats import spearmanr
from sklearn.linear_model import LinearRegression

# Tab-delimited file with columns containing overall model average REF scores, the last column containing the human scores
#The first row should be a header row
file_path = 'C:/Users/Averages for correlations.txt'  # Replace with the path to your tab-delimited file
# Read the tab-delimited file into a pandas DataFrame
data = pd.read_csv(file_path, delimiter='\t')


def calculate_spearman_correlations(data):

    # Get the list of variables (column names)
    variables = data.columns

    # Initialize an empty DataFrame to store the Spearman correlations
    correlation_matrix = pd.DataFrame(index=variables, columns=variables)

    # Calculate Spearman correlation for each pair of variables
    for var1 in variables:
        for var2 in variables:
            correlation, _ = spearmanr(data[var1], data[var2])
            correlation_matrix.loc[var1, var2] = correlation

    return correlation_matrix

correlation_matrix = calculate_spearman_correlations(data)
print(correlation_matrix)
correlation_matrix.to_csv(file_path + '_cor_matrix.csv', index=True)

def calculate_mean_absolute_deviation(data):
    # Calculate the mean absolute deviation (MAD) between each pair of columns
    variables = data.columns
    mad_matrix = pd.DataFrame(index=variables, columns=variables)

    for var1 in variables:
        for var2 in variables:
            mad = (data[var1] - data[var2]).abs().mean()
            mad_matrix.loc[var1, var2] = mad

    return mad_matrix

mad_matrix = calculate_mean_absolute_deviation(data)
print(mad_matrix)
mad_matrix.to_csv(file_path + '_MAD_matrix.csv', index=True)

def fit_linear_regression(data):
    # Get the list of variables (column names)
    variables = data.columns
    dependent_variable = variables[-1]

    regression_results = {}
    mad_values = {}

    # Fit a linear regression model for each independent variable against the dependent variable
    for independent_variable in variables[:-1]:
        X = data[[independent_variable]]
        y = data[dependent_variable]
        model = LinearRegression().fit(X, y)
        predictions = model.predict(X)
        mad = (predictions - y).abs().mean()
        regression_results[independent_variable] = {
            'coefficient': model.coef_[0],
            'intercept': model.intercept_,
            'mad': mad
        }
        mad_values[independent_variable] = mad

    return regression_results, mad_values

regression_results, regression_mad = fit_linear_regression(data)
print("\nLinear Regression Results (independent variable -> dependent variable):")
dependent_variable = data.columns[-1]
for independent_variable, result in regression_results.items():
    print(f"{independent_variable} -> {dependent_variable}: Coefficient = {result['coefficient']}, Intercept = {result['intercept']}")
regression_df = pd.DataFrame.from_dict(regression_results, orient='index')
regression_df.to_csv(file_path + 'linear_regression_results.csv', index_label='independent_variable')

print(regression_mad)
regression_mad_df = pd.DataFrame.from_dict(regression_mad, orient='index')
regression_mad_df.to_csv(file_path + 'linear_regression_mad.csv', index_label='independent_variable')
