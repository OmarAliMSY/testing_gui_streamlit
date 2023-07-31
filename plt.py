import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Long_run (3).csv")
df = df.drop(columns=["Unnamed: 0","statusNumber","errorCode"])

df.plot(x="times",y=["northSensorAngle","southSensorAngle","TiltSetAngle"])
ax = df['maxLastMotorTorque'].plot(secondary_y=True)
ax.set_ylabel('maxLastMotorTorque')

plt.show()