# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 12:22:44 2018

@author: misa
"""

import time as t
import snap7
from snap7.util import *
import matplotlib.pyplot as plt
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

#------------ INITIALIZE PLC OBJECT-------------------
plc_1=snap7.client.Client()
plc_2=snap7.client.Client()


#------------ INPUT PARAMETERS-------------------
plc_addr_1="10.49.29.104"
plc_addr_2="10.49.29.103"

area = 0x84    # area; 0x81 AI; 0x82 AO; 0x83 Merker; 0x84 DB; 0x1C Counters; 0x1D Timers

pause_time= 1 # Pause time for loop in seconds
daq_time =3000     # Data acquisition time (s)

while_end=100
while_counter=0
#------------ PREPARE INITIAL DATA-------------------
para_1=list()
para_2=list()
para_3=list()
time_list=list()

while len(para_1)<1 or while_counter<while_end:
    try:
        plc_1.connect(plc_addr_1,0,1)
        print("PLC1 can be connected?: ",plc_1.get_connected())
        plc_2.connect(plc_addr_2,0,1)
        print("PLC2 can be connected?: ",plc_1.get_connected())
        mbyte_1 = plc_1.db_read(37,2,4)                 # PLC1 data generator, DB37/2.0 REAL
        mbyte_2 = plc_2.db_read(110,94,4)               # PLC2 Tracking software, Actual wind value - DB110/94.0 REAL
        mbyte_3 = plc_2.db_read(21,0,4)                 # PLC2 Tracking software, Norm filtered - DB21/0.0 REAL
        
        para_1.append(snap7.util.get_real(mbyte_1,0))
        para_2.append(snap7.util.get_real(mbyte_2,0))
        para_3.append(snap7.util.get_real(mbyte_3,0))
        time_start=t.time()        
        time_list.append(time_start-time_start)
        plc_1.disconnect()
        plc_2.disconnect()
    except:
        print('Exception raised at Initialisation ')
        while_counter=while_counter+1
        continue
    break

rng=daq_time/pause_time
start_time=t.time()
while_counter=0
plt.figure(0)
plt.ion()
plt.xlabel('Time (s)')
plt.ylabel('mA or m/s')
plt.plot(time_list,para_1,c='b',label='V20_1 Data Generator')
plt.plot(time_list,para_2,c='r',label='V20_2 with filter')
plt.plot(time_list,para_3,c='g',label='PLC2 with Norm Filter')
plt.legend(loc=1)
plt.grid(linestyle='-')
plt.title('Monitoring Wind values')

print('Initialisation done! - Starting DAQ!')
#------------ START DAQ LOOP-------------------
plc_1.connect(plc_addr_1,0,1)
plc_2.connect(plc_addr_2,0,1)
for i in range(int(rng)):

    while while_counter<while_end:
        try:
            #plc_1.connect(plc_addr_1,0,1)
            #plc_2.connect(plc_addr_2,0,1)
            mbyte_1 = plc_1.db_read(37,2,4)                 # PLC1 data generator, DB37/2.0 REAL
            mbyte_2 = plc_2.db_read(110,94,4)               # PLC2 Tracking software, Actual wind value - DB110/94.0 REAL
            mbyte_3 = plc_2.db_read(21,0,4)                 # PLC2 Tracking software, Norm filtered - DB21/0.0 REAL
        
            para_1.append(snap7.util.get_real(mbyte_1,0))
            para_2.append(snap7.util.get_real(mbyte_2,0))
            para_3.append(snap7.util.get_real(mbyte_3,0))
            
            time_list.append(t.time()-time_start)
                        
            plt.plot(time_list[-2:],para_1[-2:],c='b',linewidth=1)
            plt.plot(time_list[-2:],para_2[-2:],c='r',linewidth=1)
            plt.plot(time_list[-2:],para_3[-2:],c='g',linewidth=1)
            
            #plc_1.disconnect()
            #plc_2.disconnect()
            
            plt.show()
            plt.pause(pause_time)
            
        except snap7.snap7exceptions.Snap7Exception:
            print('Exception raised in DAQ')
            while_counter=while_counter+1
            continue
        except KeyboardInterrupt:
            print('*** Keyboard Interrupt from user ***')
            while_counter=while_end+1
            break
        break

plt.show()
plc_1.disconnect()
plc_2.disconnect()
print("PLC1 connected: ",plc_1.get_connected())
print("PLC2 connected: ",plc_2.get_connected())
end_time=t.time()
total_time=end_time-start_time
print("END - ","Time taken: ", total_time," sec")

print('Save data to excel? (y/n)')
save_data=input()
df=pd.DataFrame({'time':time_list,
     'para_1':para_1,
     'para_2':para_2,
     'para_3':para_3})
if save_data=='y':
    print('Input file name to save & press Enter:')
    dataname=input()
    writer=ExcelWriter(dataname+'.xls')
    df.to_excel(writer,'Sheet1',index=False)
    writer.save()
    print('Data Saved as ',dataname,'.xls')
elif save_data=='n':
    print('Data not saved as excel! Exiting code! Please save data (dataframe df) manually!')
else:
    print('Wrong input!, exiting code! Please save data (dataframe df) manually!')