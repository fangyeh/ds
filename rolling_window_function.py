import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_running_total(df):
    # First Step: Clean the Data
    # filter for DSP
    df = df.loc[df['CHANNEL'] == 'DSP']

    # Drop rows with null values in 'COST' column
    df = df.dropna(subset=['COST'])

    # Remove rows where 'COST' is 0
    df = df[(df['COST'] != 0) & (df['ORDERS'] != 0)]

    # Second Step: Create Calculated Fields and Filter the Data
    # convert DATE to datetime object
    df['DATE'] = pd.to_datetime(df['DATE'])
    # create ROAS and CPA
    df['ROAS'] = df['REVENUE'] / df['COST']
    df['CPA'] = np.where(df['ORDERS'] == 0, 0, df['COST'] / df['ORDERS'])

    # Third Step: Select Desired Segement of the Data
    # Input time period
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    df = df.loc[df['DATE'].between(start_date, end_date)]

    # Input Funnel Stage(s)
    funnel_stages = input("Enter funnel stages separated by comma (e.g., Awareness,Consideration): ").split(',')
    df = df.loc[df['FUNNEL'].str.contains('|'.join(funnel_stages), case=False)]

    # Fourth Step: Plot The Data: Needs to Input the window for both COST and ORDERS column
    window_size = int(input("Enter window size for rolling sum: "))

    # Assuming df_grouped is already defined as per your code
    df_grouped = df.groupby('DATE').agg({'COST': 'sum', 'ORDERS': 'sum', 'ROAS': 'mean', 'CPA': 'mean'}).reset_index()
    # Calculate the running total of COST for each 14-day interval
    df_grouped['Running_Total_COST'] = df_grouped['COST'].rolling(window=window_size, min_periods=1).sum()

    # Calculate the running total of ORDERS for each 14-day interval
    df_grouped['Running_Total_ORDERS'] = df_grouped['ORDERS'].rolling(window=window_size, min_periods=1).sum()

    # Plot the running total of COST
    fig, ax1 = plt.subplots(figsize=(12, 6))

    color = 'tab:red'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Running Total COST', color=color)
    ax1.plot(df_grouped['DATE'], df_grouped['Running_Total_COST'], color=color, linestyle='-.', label='Running Total COST')
    ax1.tick_params(axis='y', labelcolor=color)

    # Create a secondary y-axis for the CPA
    # ax2 = ax1.twinx()
    # color = 'tab:blue'
    # ax2.set_ylabel('CPA', color=color)
    # ax2.plot(df_grouped['DATE'], df_grouped['CPA'], linestyle='--', color=color, label='CPA')
    # ax2.tick_params(axis='y', labelcolor=color)


    # Create a third y-axis for ORDERS
    ax3 = ax1.twinx()
    color = 'tab:green'
    ax3.set_ylabel('Running Total ORDERS', color=color)
    ax3.plot(df_grouped['DATE'], df_grouped['Running_Total_ORDERS'], linestyle='--', color=color, label='Running Total ORDERS')
    ax3.tick_params(axis='y', labelcolor=color)

    # Get the current y-axis tick labels
    yticks = ax1.get_yticks()

    # Convert the tick labels to the original number format
    yticklabels = [f'{int(ytick):,}' for ytick in yticks]

    # Set the new tick labels
    ax1.set_yticklabels(yticklabels)

    # Add a legend
    fig.tight_layout()
    fig.legend(loc='upper right')
    plt.show()

# Example usage:
# plot_running_total(df)
