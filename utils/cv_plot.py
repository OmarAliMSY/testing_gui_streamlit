import pandas as pd
import matplotlib.pyplot as plt

csv_path = r'C:\Users\o.abdulmalik\Documents\testing_gui\Lebensdauertest_231204.csv'
df = pd.read_csv(csv_path, parse_dates=['times'], index_col=['times'])

# Define thresholds and tolerance
upper_threshold = 60
lower_threshold = -60
tolerance = 0.5

# Function to find threshold crossings
def find_crossings(series, threshold, tolerance):
    crossing = series[(series.shift(1) < threshold - tolerance) & (series >= threshold - tolerance) |
                      (series.shift(1) > threshold + tolerance) & (series <= threshold + tolerance)]
    return crossing.index

# Find crossings
crossings_lower = find_crossings(df['northSensorAngle_t2'], lower_threshold, tolerance)
crossings_upper = find_crossings(df['northSensorAngle_t2'], upper_threshold, tolerance)

# List to store cycles
cycles = []

# Iterate over lower crossings to find complete cycles
for start in crossings_lower:
    # Find the next upper crossing after this lower crossing
    next_upper_crossing = crossings_upper[crossings_upper > start].min()

    # Find the next lower crossing after the upper crossing
    next_lower_crossing = crossings_lower[crossings_lower > next_upper_crossing].min()

    # Check if the cycle is valid
    if pd.notna(next_upper_crossing) and pd.notna(next_lower_crossing):
        cycle = df.loc[start:next_lower_crossing]
        cycles.append(cycle)
num_cycles_to_combine = 2
angle_diff = df['northSensorAngle_t2'].diff()

# Calculate the time difference in seconds
time_diff = df.index.to_series().diff().dt.total_seconds()
# Calculate the velocity: angular change per unit time (degrees per second)
df['velocity'] = angle_diff / time_diff

# Check if there are enough cycles to combine
if len(cycles) >= num_cycles_to_combine:
    # Combine the first 20 cycles
    combined_cycles = pd.concat(cycles[:num_cycles_to_combine])
else:
    # If there are fewer than 20 cycles, combine as many as available
    combined_cycles = pd.concat(cycles)

df['velocity'] = df['velocity'][combined_cycles.index[0]:combined_cycles.index[-1]] *60
df['velocity']= abs(df['velocity'].rolling(30).mean() )
print(cycles[0].index[-1])
# Example: Plotting the first cycle
if cycles:
    df['velocity'].plot(title='Angular Velocity over Time (2 Cycles)')

    combined_cycles['northSensorAngle_t2'].plot(title='Four Cycles')
    plt.xlabel('Time')
    plt.ylabel('Angle Velocity [°/min]')
    plt.show()
else:
    print("No complete cycles found.")
