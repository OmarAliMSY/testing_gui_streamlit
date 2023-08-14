import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r"csv_data\server\csv_data\newtimestamp.csv")

df = df.drop(columns=["statusNumber", "errorCode"])
fig, ax = plt.subplots(figsize=(20, 10))

# Plot the columns
df.plot(x="times", y=["northSensorAngle", "southSensorAngle", "TiltSetAngle"], ax=ax)
#df.plot(x="times", y="maxLastMotorTorque", secondary_y=True, ax=ax, color="blue")

# Adjust x-axis labels
num_ticks = 10  # You can adjust the number of ticks as needed
x_ticks_indices = range(0, len(df), len(df) // num_ticks)
x_tick_labels = df["times"].apply(lambda x: x.split()[1]).iloc[x_ticks_indices]
plt.xticks(x_ticks_indices, x_tick_labels)  # No rotation and alignment for now

# Rotate and align labels
plt.gcf().autofmt_xdate(rotation=45, ha="right")  # Rotate and align after setting xticks

plt.show()





