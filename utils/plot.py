import pandas as pd
import matplotlib.pyplot as plt
from glob import glob
import re
import numpy as np

csv_path = glob(r"C:\Users\o.abdulmalik\Documents\testing_gui\csv_data\231012\*.csv")
for csv_file in csv_path:
    df = pd.read_csv(csv_file,parse_dates=True)
    kg = re.findall(r'\d+', csv_file)[-1]
    xticks = list(np.linspace(0,len(df["times"])-1,5))
    print(xticks)
    df["torque_abs"] = df["torque_abs"].rolling(3).mean()*5/2
    ax = df.plot(x="times",y=["northSensorAnglet2"],title=f"{kg} [kg]", xlabel="time", ylabel="Angle [°]",figsize=(13, 5))
    df.plot(x="times",y=["torque_abs"], ylabel="Torque [Nm]",secondary_y=True,ax=ax)
    ax.set_xticks(xticks)
    ax.set(xticklabels = df["times"].iloc[xticks])
    plt.show()