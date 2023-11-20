import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob
from datetime import datetime
from matplotlib.dates import DateFormatter, MinuteLocator
import re 

# Define the folder containing the CSV files
folder_path = r"C:\Users\o.abdulmalik\Documents\testing_gui\csv_data\231012"

# Define the date format as a string
date_format = '%Y-%m-%d %H:%M:%S'

# Get a list of all CSV files in the folder
csv_paths = glob(f"{folder_path}/*.csv")
calculated_valuesew = {     "715" :     [-28.30 ,-8.36,6.30,17.74 ,27.11 ,35.12 ,-52.95,-61.72,-71.13,-82.59 ],  #same dir
                            "1465" :    [ 7.93    ,29.17   ,44.31   ,55.70   ,64.63   ,71.96   ,-97.95  ,-105.62 ,-114.03 ,-124.87 ],
                            "2865" :    [75.57 , 99.21 , 115.26, 126.55, 134.69, 140.73],
                            "3425" :    [102.63  ,127.23  ,143.64  ,154.89  ,162.71  ,168.24  ,-215.54 ,-220.32 ,-226.15 ,-235.36 ]
                            }
calculated_valueswe = {     "715" :     [ 35.38 ,10.44 ,-7.88 ,-22.18,-33.88,-43.90,42.36 ,49.38 ,56.90, 66.07  ], 
                            "1465" :    [-9.92 , -36.46, -55.39, -69.62, -80.79, -89.95, 78.36 , 84.49 , 91.23 , 99.90],
                            "2865" :    [-94.47  , -124.01 , -144.07 , -158.19 , -168.36 , -175.92 ],
                            "3425" :    [-128.29, -159.04, -179.55, -193.61, -203.38, -210.30, 172.44, 176.26, 180.92, 188.29 ]
                            }


calc_angles = np.arange(-50,50,10,)
calc_angles_2865 = np.arange(-50,10,10)
print(calc_angles_2865.shape,calc_angles)
# Create a single figure for all subplots
fig, axs = plt.subplots(len(csv_paths), 2, figsize=(12, 4 * len(csv_paths)))

# Define the number of subplots per row
subplots_per_row = 2
axs[0, 0].set_title(f'Torque West to East')
axs[0, 1].set_title(f'Torque East to West')
meanlist1, meanlist2 = [],[]
kglist = []

# Create subplots for each pair of CSV files
for i, csv_path in enumerate(csv_paths):
    # Read the CSV file
    df = pd.read_csv(csv_path, parse_dates=True)
    kg = re.findall(pattern=r"\d+",string=csv_path)
    print(kg[-1])
    angle = df["northSensorAnglet2"]
    if kg[-1] == "3425":
        torque = df["torquet2"].rolling(10).mean() * -110
    else:
        torque = ((df["torque_percentage"]* 400) - 200) 
        #torque = df["torque_percentage"].rolling(10).mean()
    times = df["times"]
    angle = np.array(df["northSensorAnglet2"],dtype=np.float16)
    times = [datetime.strptime(time, date_format) for time in times]
    if kg[-1] == "2865":
        w = -0
        e = -51
    else:
        
        e = -51
        w = 40
    sort_idx = np.abs(np.abs(angle - w))
    idx = np.argsort(sort_idx)[:2]

    differences = np.abs(angle - e)
    closest_indices = np.argsort(differences)[:2]
    idx = np.sort(np.array(idx))
    closest_indices = np.sort(np.array(closest_indices))

    non_zero_torque = torque[closest_indices[0]:idx[0]][torque[closest_indices[0]:idx[0]] != 0]

    mean_value1 = np.abs(np.mean(non_zero_torque)         ) 
    axs[i, 1].plot(np.array(angle)[closest_indices[0]:idx[0]], np.abs(torque[closest_indices[0]:idx[0]]),label=f"Torque {kg[-1]} kg",c="green")
    axs[i, 1].hlines(mean_value1, xmin=np.array(angle)[closest_indices[0]], xmax=np.array(angle)[idx[0]],label=f"Mean Torque {np.round(mean_value1)}")
    axs[i, 1].invert_xaxis()
    #axs[i, 1].set_ylim(bottom=mean_value1-mean_value1/3, top=mean_value1+mean_value1/3)

    calculated_valueswe[kg[-1]] = [val *1 for val in calculated_valueswe[kg[-1]] ]
    if kg[-1] =="2865":
        axs[i,1].plot(calc_angles_2865,np.abs(calculated_valueswe[kg[-1]]) ,label= "Calculated Torque",c="orange")
        axs[i,0].plot(calc_angles_2865,np.abs(calculated_valuesew[kg[-1]]) ,label= "Calculated Torque",c="orange")

    else:

        axs[i,1].plot(calc_angles,np.abs(calculated_valueswe[kg[-1]]) ,label= "Calculated Torque",c="orange")
        axs[i,0].plot(calc_angles,np.abs(calculated_valuesew[kg[-1]]) ,label= "Calculated Torque",c="orange")



    
    meanlist1.append(mean_value1)
    kglist.append(kg[-1])
    
    non_zero_torque = torque[idx[1]:closest_indices[1]][torque[idx[1]:closest_indices[1]] != 0]
    mean_value2 = np.abs(np.mean(non_zero_torque[100:]))
    meanlist2.append(mean_value2)

    axs[i, 0].plot(np.array(angle)[idx[1]:closest_indices[1]], np.abs(torque[idx[1]:closest_indices[1]]),c="green")
    axs[i, 0].hlines(mean_value2, xmin=np.array(angle)[idx[1]], xmax=np.array(angle)[closest_indices[1]],label=f'Mean Torque {np.round(mean_value2)}')
    axs[i, 1].legend(loc='upper left', bbox_to_anchor=(1, 0.5))
    #axs[i, 0].set_ylim(bottom=mean_value2+mean_value2/5, top=mean_value2-mean_value2/5)

    axs[i, 0].legend(loc="best")

    

    axs[len(csv_paths)-1, 1].set_xlabel('Angle')
    axs[len(csv_paths)-1, 0].set_xlabel('Angle')

for i in range(len(csv_paths)):
    axs[i, 0].set_ylabel('Torque')
    axs[i, 1].set_ylabel('Torque')
    


    

#plt.tight_layout()

plt.show()
plt.plot(kglist,meanlist1,label="West to East")
plt.scatter(kglist,meanlist1,marker="o")
plt.xlabel("Weight on East Side [kg]")
plt.ylabel("Torque [Nm]")
plt.plot(kglist,np.abs(meanlist2),label="East to West")
plt.scatter(kglist,np.abs(meanlist2),marker="o")

plt.legend()
plt.show()
