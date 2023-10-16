import pandas as pd
import matplotlib.pyplot as plt
from glob import glob
import re
import matplotlib.dates as mdates
import matplotlib.ticker as mticker


csv_paths = glob("csv_data/231012/*.csv")
m_list = []

# Determine the number of subplots needed
num_plots = len(csv_paths)
num_cols = 3  # Number of columns in the grid
num_rows = (num_plots + num_cols - 1) // num_cols

# Create a grid of subplots
fig, axs = plt.subplots(num_rows, num_cols, figsize=(15, 5 * num_rows))

# Flatten axs if it's a 1D array
if num_rows == 1:
    axs = [axs]

for i, csv_file in enumerate(csv_paths):
    kg = re.findall(r'\d+', csv_file)[-1]
    m_list.append(kg)
    df = pd.read_csv(csv_file)
    row_idx = i // num_cols
    col_idx = i % num_cols
    ax = axs[row_idx][col_idx]
    
    ax.plot(df["times"], df["northSensorAnglet2"], label=f"Angle {kg} kg")
    ax.plot(df["times"], df["torque_abs"], label=f"Torque {kg} kg")
    ax.set_title(f"Weight: {kg} kg")
    ax.legend()
    n = i
    num_ticks = 10
    x_ticks_indices = range(0, len(df), len(df) // num_ticks)
    x_tick_labels = df["times"].iloc[x_ticks_indices]
    ax.set_xticks(x_ticks_indices)
    ax.set_xticklabels(x_tick_labels, rotation=45, ha="right")




    plt.gcf().autofmt_xdate(rotation=45, ha="right")
# Adjust layout
plt.tight_layout()

# Show the plot
plt.show()
