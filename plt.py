import pandas as pd
import matplotlib.pyplot as plt
import time


df = pd.read_csv(r"csv_data\omarstes123t.csv")
df = df.drop(columns=["statusNumber","errorCode"])
df['times'] = df['times'].apply(lambda ts: time.strftime("%H:%M:%S", time.localtime(ts)))

fig, ax = plt.subplots(figsize=(20,10)) 

df.plot(x= "times",y=["northSensorAngle","southSensorAngle","TiltSetAngle"],ax=ax)
df.plot(x="times",y="maxLastMotorTorque",secondary_y=True,ax=ax,color="blue")

plt.show()