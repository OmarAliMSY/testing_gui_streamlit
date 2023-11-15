import pandas as pd
import matplotlib.pyplot as plt
from glob import glob
import numpy as np


csv_path = glob(r"C:\Users\o.abdulmalik\Documents\testing_gui\csv_data\server\csv_data\Lebensdauertest_231108.csv")
df = pd.read_csv(csv_path[0], parse_dates=["times"], index_col=["times"])


#xticks = list(np.linspace(0, len(df["times"]) - 1, len(df["times"])//1000))
df["torque_t2"] = df["torque_t2"].rolling(3).mean() * 110
ax = df.plot( y=["torque_t2"], xlabel="time", ylabel="Torque [Nm]", figsize=(13, 5))
df.plot( y=["northSensorAngle_t2"], ylabel="Angle [°]", secondary_y=True, ax=ax)


# Adding legend to the plot
plt.legend(loc='upper left')


plt.show()
