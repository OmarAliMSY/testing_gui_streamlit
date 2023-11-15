import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob
from datetime import datetime
from matplotlib.dates import DateFormatter, MinuteLocator
import re 

# Define the folder containing the CSV files
folder_path = r"C:\Users\o.abdulmalik\Documents\testing_gui\csv_data\231017"

# Define the date format as a string
date_format = '%Y-%m-%d %H:%M:%S'

# Get a list of all CSV files in the folder
csv_paths = glob(f"{folder_path}/*.csv")

calculated_valuesew = { "0" :       [ 8.95, 6.40, 4.21, 2.13, 0, -2.3, -4.88, -7.92, -11.68,-16.63], 
                        "715" :     [-106.36, -86.20, -70.44, -57.26, -45.69, -35.12, 31.41, 19.13, 6.36, -8.01], 
                        "1465" :    [ -152.00, -130.32, -112.93, -97.98 , -84.51 , -71.96 , 74.91  , 60.04  , 44.74  , 27.95 ],
                        "2865" :    [-237.21, -212.70, -192.24, -173.98, -156.99, -140.73,  156.10,  136.42,  116.39,  95.06]}

calculated_valueswe = { "0" :       [ 8.95, 6.40, 4.21, 2.13, 0, -2.3, -4.88, -7.92, -11.68,-16.63], 
                        "715" :     [ 132.95, 107.75, 88.05, 71.57, 57.11, 43.90, -25.13, -15.30, -5.09, 6.40], 
                        "1465" :    [ 190.01, 162.91, 141.16, 122.47, 105.64, 89.95 , -59.93, -48.03, -35.79, -22.36 ],
                        "2865" :    [296.51,265.87,240.30,217.48,196.23,175.92, -124.88, -109.14, -93.11, -76.05]}


calc_angles = np.arange(-40,60,10,)
fig, axs = plt.subplots(len(csv_paths), 2, figsize=(12, 4 * len(csv_paths)))

# Define the number of subplots per row
subplots_per_row = 2
axs[0, 0].set_title(f'Torque from East to West')
axs[0, 1].set_title(f'Torque from West to East')
meanlist1, meanlist2 = [],[]
kglist = []

# Create subplots for each pair of CSV files
for i, csv_path in enumerate(csv_paths):
    # Read the CSV file
    df = pd.read_csv(csv_path, parse_dates=True)
    kg = re.findall(pattern=r"\d+",string=csv_path)
    print(kg[-1])
    angle = df["northSensorAnglet2"]
    
    torque = df["torquet2"].rolling(15).mean() * -110
    
    times = df["times"]
    angle = np.array(df["northSensorAnglet2"],dtype=np.float16)
    times = [datetime.strptime(time, date_format) for time in times]
    w = -39
    e = 50
    sort_idx = np.abs(np.abs(angle - w))
    idx = np.argsort(sort_idx)[:2]

    differences = np.abs(angle - e)
    closest_indices = np.argsort(differences)[:2]
    idx = np.sort(np.array(idx))
    closest_indices = np.sort(np.array(closest_indices))

    non_zero_torque = torque[closest_indices[0]:idx[0]][torque[closest_indices[0]:idx[0]] != 0]

    mean_value1 = np.abs(np.mean(non_zero_torque)     )     
    axs[i, 0].plot(np.array(angle)[closest_indices[0]:idx[0]], np.abs(torque[closest_indices[0]:idx[0]]),label=f"Torque {kg[-1]} kg",c="green")
    axs[i, 0].hlines(mean_value1, xmin=np.array(angle)[closest_indices[0]], xmax=np.array(angle)[idx[0]],label=f"Mean Torque {np.round(mean_value1)}")
    axs[i, 0].legend(loc="best")
    axs[i, 0].invert_xaxis()
    #axs[i, 0].set_ylim(bottom=mean_value1+mean_value1/5, top=mean_value1-mean_value1/5)

    #calculated_valueswe[kg[-1]] = [val *-1 for val in calculated_valueswe[kg[-1]] ]

    
    meanlist1.append(mean_value1)
    kglist.append(kg[-1])
    
    non_zero_torque = torque[idx[1]:closest_indices[1]][torque[idx[1]:closest_indices[1]] != 0]
    mean_value2 = np.abs(np.mean(non_zero_torque[100:]))
    meanlist2.append(mean_value2)

    axs[i, 1].plot(np.array(angle)[idx[1]:closest_indices[1]], np.abs(torque[idx[1]:closest_indices[1]]),c="green")
    axs[i, 1].hlines(mean_value2, xmin=np.array(angle)[idx[1]], xmax=np.array(angle)[closest_indices[1]],label=f'Mean Torque {np.round(mean_value2)}')
    axs[i, 1].legend(loc="best")
    #axs[i, 1].set_ylim(bottom=mean_value2-mean_value2/5, top=mean_value2+mean_value2/5)

    axs[i,1].plot(calc_angles,np.abs(calculated_valuesew[kg[-1]]) ,label= "Calculated Torque",c="orange")

    axs[i,0].plot(calc_angles,np.abs(calculated_valueswe[kg[-1]]) ,label= "Calculated Torque",c="orange")

    

    axs[len(csv_paths)-1, 1].set_xlabel('Angle')
    axs[len(csv_paths)-1, 0].set_xlabel('Angle')

for i in range(len(csv_paths)):
    axs[i, 0].set_ylabel('Torque')
    


    

#plt.tight_layout()

plt.show()
plt.plot(kglist,meanlist1,label="East to West")
plt.scatter(kglist,meanlist1,marker="o")
plt.xlabel("Weight on East Side [kg]")
plt.ylabel("Torque [Nm]")
plt.plot(kglist,np.abs(meanlist2),label="West to East")
plt.scatter(kglist,np.abs(meanlist2),marker="o")

plt.legend()
plt.show()
