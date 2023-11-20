import pandas as pd
import matplotlib.pyplot as plt
from glob import glob
import numpy as np


csv_path = glob(r"C:\Users\o.abdulmalik\Documents\testing_gui\csv_data\7m231108.csv")
df = pd.read_csv(csv_path[0], parse_dates=["times"], index_col=["times"])


df["torque_percentage"] = (((df["torque_percentage"]) * 400 ) -200) * 7
print(np.mean(df["torque_abs"]))

df["torque_t1"] = np.abs(df["torque_t1"].rolling(3).mean() * 110)
df["torque_percentage"] = np.abs(df["torque_percentage"].rolling(3).mean())

ax = df.plot( y=["torque_t1","torque_percentage"], xlabel="time", ylabel="Torque [Nm]", figsize=(13, 5))
df.plot( y=["northSensorAngle_t1"], ylabel="Angle [°]", secondary_y=True, ax=ax)




plt.show()
