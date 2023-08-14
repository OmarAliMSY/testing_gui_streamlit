import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np

df = pd.read_csv(r"csv_data\server\Omarstest123.csv")
x = np.linspace(0,1,len(df["statusNumber"]))
df = df.drop(columns=["statusNumber","errorCode"])
#df['times'] = df['times'].apply(lambda ts: time.strftime("%H:%M:%S", time.localtime(ts)))
fig, ax = plt.subplots(figsize=(20,10)) 
plt.plot(x,df["maxLastMotorTorque"])

#df.plot(x= "times",y=["northSensorAngle","southSensorAngle","TiltSetAngle"],ax=ax)
#df.plot(x="times",y="maxLastMotorTorque",secondary_y=True,ax=ax,color="blue")

plt.show()