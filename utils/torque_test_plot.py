import pandas as pd
import matplotlib.pyplot as plt
from glob import glob
import numpy as np
import seaborn as sns
from matplotlib import cm as cm

csv_path = r'C:\Users\o.abdulmalik\Documents\testing_gui\csv_data\torque_tests\Torquetest_231219_fullweight_2.csv'

df = pd.read_csv(csv_path, parse_dates=['times'], index_col=['times'])

stats = df.describe()
print(stats.columns)
stats = stats.drop(axis=1,labels=['errorCode_t2','errorCode_t1','statusNumber_t2','statusNumber_t1',"actualeDeltaPhi_t2",
                                  "southSensorAngle_t2", "actualFrequency_t1",'sensor2Offset_t2', 'sensor1Offset_t2'])
stats = stats.drop(axis=1,labels=[p for p in stats.keys() if "t2" in p])
print(stats.columns)
#sns_plot = sns.heatmap(stats, annot=True,fmt='.1f',xticklabels=stats.keys(),)
ax = sns.heatmap(stats.T, annot=True,robust=True,vmax=100)
ax.set(xlabel="", ylabel="")
    # save to file
df['Torque_Sensor'] = (((df['torque_percentage']) *400 )- 200) 

df['torque_t1'] = np.abs(df['torque_t1'].rolling(1).mean() ) * 110 
df['Torque_Sensor'] = np.abs(df['Torque_Sensor'].rolling(1).mean()) *7/3

ax = df.plot( y=['torque_t1','Torque_Sensor'], xlabel='time', ylabel='Torque [Nm]', figsize=(13, 5))
df.plot( y=['northSensorAngle_t1'], ylabel='Angle [°]', secondary_y=True, ax=ax)

plt.show()