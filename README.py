import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
from scipy.stats import gaussian_kde
from ipywidgets import interact, widgets

# Function to plot the interactive chart
def plot_interactive_chart(file_path, last_days):
    df = pd.read_excel(file_path)

    # Assuming you have Date column
    df['Date'] = pd.to_datetime(df['Date'])

    # Filter your Date column
    last_days_data = df[df['Date'] >= (df['Date'].max() - pd.Timedelta(days=last_days))]

    # Extract the 'Sale' column from the DataFrame
    sales_data = last_days_data['Sale']

    # Set the figure size for better quality
    plt.figure(figsize=(24, 8))

    # Create a KDE plot with enhanced quality
    sns.kdeplot(sales_data, fill=True, color='b', label='Sales Distribution', linewidth=2)

    # Customize the color palette
    sns.set_palette("husl")

    # Multiply the Probability Density values by 1000 to make them more interpretable
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x * 100000:.1f}'))

    # Calculate the KDE
    kde = gaussian_kde(sales_data)
    x = np.linspace(sales_data.min(), sales_data.max(), 1000)
    y = kde(x)

    # Find the x-coordinate of the maximum probability
    max_prob_index = np.argmax(y)
    max_prob_value = x[max_prob_index]

    # Add a vertical line at the highest probability point
    plt.axvline(max_prob_value, color='r', linestyle='--', label=f'Max Probability Point: {max_prob_value:.2f}', linewidth=2)

    # Display the highest probability (multiplied by 100,000) next to the max probability point
    plt.annotate(f'Highest Probability: {max(y) * 100000:.5f}', (max_prob_value, kde(max_prob_value)),
                 textcoords="offset points", xytext=(20, 30), ha='center', fontsize=12, color='r')

    # Label the axes and title
    plt.xlabel('Sales Amount')
    plt.ylabel('Probability')
    plt.title('')

    # Add a text annotation for the highest probability value (as currency) at the peak of the line chart
    plt.annotate(f'${max_prob_value:,.2f}', (max_prob_value, kde(max_prob_value)), textcoords="offset points",
                 xytext=(50, 6), ha='center', fontsize=16, color='r')

  # Remove all spines (lines around the chart)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)


    # Add a legend
    plt.legend()

    # Enable grid lines
    plt.grid(False)

    # Show the plot
    plt.show()

# File path dropdown widget with readable names
file_path_dropdown = widgets.Dropdown(
    options={
        'Product A': 'your_source_file1.xlsx',
        'Product B': 'your_source_file2.xlsx',
        'Product C' :'your_source_file3.xlsx'
    },
    value='your_source_file1.xlsx',
    description='File Path:'
)

# Last days dropdown widget
last_days_dropdown = widgets.Dropdown(
    options=[30, 60],
    value=30,
    description='Last Days:'
)

# Interactive plot function
interact(plot_interactive_chart, file_path=file_path_dropdown, last_days=last_days_dropdown)





