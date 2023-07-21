import os
import matplotlib.pyplot as plt
import base64

output_html = 'output/report.html'
css_file = 'styles.css'

# Get the absolute path of the CSS file
css_path = os.path.abspath(css_file)

def plot_numerical_data(data,sampledata,numb_columns, html_report):
    for col in numb_columns:
        # Create a new figure
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(6, 3))
        # Numerical column, plot histograms
        axes[0].hist(data[col], bins=50, alpha=0.5, label='Full Data', density=True, color='#01669a')
        axes[0].set_xlabel(col)
        axes[0].set_ylabel('Frequency')
        axes[0].set_title(f'Full Data - {col}')
        # axes[0].legend()

        axes[1].hist(sampledata[col], bins=50, alpha=0.5, label='Sample Data', density=True, color='#01669a')
        axes[1].set_xlabel(col)
        axes[1].set_ylabel('Frequency')
        axes[1].set_title(f'Sample Data - {col}')
        # Adjust the spacing between subplots
        fig.tight_layout()
        # Generate a unique file name based on the column name
        file_name = f'output/plots/distributions_of_{col}.png'

        # Save the figure as an image file
        fig.savefig(file_name)

        # Read the saved image file
        with open(file_name, 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        # Add the plot to the HTML report
        html_report.write(f'<h2>Distributions of {col}</h2>\n')
        html_report.write(f'<img src="data:image/png;base64,{encoded_image}">\n')

        # Close the figure to release memory
        plt.close(fig)


def plot_categorical_data(data,sampledata,cat_columns, html_report):
   for col in cat_columns:
        # Create a new figure
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(6, 3))
        # Categorical column, plot bar plots
        data[col].value_counts(normalize=True).plot(kind='bar', ax=axes[0],color='#01669a')
        axes[0].set_xlabel(col)
        axes[0].set_ylabel('Frequency')
        axes[0].set_title(f'Full Data - {col}')

        sampledata[col].value_counts(normalize=True).plot(kind='bar', ax=axes[1],color='#01669a')
        axes[1].set_xlabel(col)
        axes[1].set_ylabel('Frequency')
        axes[1].set_title(f'Sample Data - {col}')

        # Adjust the spacing between subplots
        fig.tight_layout()
       # Generate a unique file name based on the column name
        file_name = f'output/plots/distributions_of_{col}.png'

        # Save the figure as an image file
        fig.savefig(file_name)

        # Read the saved image file
        with open(file_name, 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        # Add the plot to the HTML report
        html_report.write(f'<h2>Distributions of {col}</h2>\n')
        html_report.write(f'<img src="data:image/png;base64,{encoded_image}">\n')

        # Close the figure to release memory
        plt.close(fig)

def run_report(full_data, sample_data, numeric_columns, categorical_columns, sizes,
               mean_df, std_df, corr_full_data_df, corr_sample_data_df, ks_results_df, chi2_results_df):
    # Open the HTML report file for writing
    with open(output_html, 'w') as html_report:
        # Write the CSS link in the head section
        html_report.write('<head>\n')
        html_report.write(f'<link rel="stylesheet" href="{css_path}">\n')
        html_report.write('<style>\n')
        html_report.write('.container {\n')
        html_report.write('    display: flex;\n')
        html_report.write('    justify-content: center;\n')
        html_report.write('    align-items: center;\n')
        html_report.write('    flex-direction: column;\n')
        html_report.write('    text-align: center;\n')
        html_report.write('}\n')
        html_report.write('</style>\n')
        html_report.write('</head>\n')

        # Wrap the report content in a container div
        html_report.write('<div class="container">\n')
        html_report.write('<h1>Comparison of Data Statistics of Full Cyclistic Data and Sample Cyclistic Data</h1>\n\n')
        # Close the container div
        html_report.write('</div>\n')

        # Wrap the report content in a container div
        html_report.write('<div class="container">\n')

        html_report.write('<h2>Datasets Sizes</h2>\n')
        html_report.write(sizes.to_html(justify='center', classes='table table-striped', na_rep='NaN'))

        html_report.write('<h2>Mean Values</h2>\n')
        html_report.write(mean_df.to_html(justify='center', classes='table table-striped', na_rep='NaN'))

        html_report.write('<h2>Standard Deviations</h2>\n')
        html_report.write(std_df.to_html(justify='center', classes='table table-striped', na_rep='NaN'))

        html_report.write('<h2>Correlation Matrices</h2>\n')
        html_report.write('<h3>Full Data</h3>\n')
        html_report.write(corr_full_data_df.to_html(justify='center', classes='table table-striped', na_rep='NaN'))
        html_report.write('<h3>Sample Data</h3>\n')
        html_report.write(corr_sample_data_df.to_html(justify='center', classes='table table-striped', na_rep='NaN'))

        html_report.write('<h2>Kolmogorov-Smirnov Test for Distribution Comparison of Numerical Columns</h2>\n')
        html_report.write(ks_results_df.to_html(justify='center', classes='table table-striped', na_rep='NaN'))
        html_report.write('<h2>Chi-square Test for Distribution Comparison of Categorical Columns</h2>\n')
        html_report.write(chi2_results_df.to_html(justify='center', classes='table table-striped', na_rep='NaN'))

        # Open the plot container div with scrolling capability
        html_report.write('<div class="plot-container">\n')

        # Generate and add plots for numerical columns
        plot_numerical_data(full_data, sample_data, numeric_columns, html_report)

        # Generate and add plots for categorical columns
        plot_categorical_data(full_data, sample_data, categorical_columns, html_report)

        # Close the plot container div
        html_report.write('</div>\n')

        # Close the container div
        html_report.write('</div>\n')
