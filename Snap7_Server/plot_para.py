# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 12:22:44 2018

@author: misa
"""

import time as t
import snap7
from snap7.util import *
import matplotlib.pyplot as plt

#------------ INITIALIZE PLC OBJECT-------------------
plc=snap7.client.Client()


#------------ INPUT PARAMETERS-------------------
plc_addr="10.49.61.85"
tcpport=1102
area = 0x84    # area; 0x81 AI; 0x82 AO; 0x83 Merker; 0x84 DB; 0x1C Counters; 0x1D Timers
db_number = 110  # dbnumber
start = 0      # start reading from this point in DB
length = 3668-start     # length in bytes of the read (reading 3 real values after start)
pos_1=2706-start
pos_2=2710-start
pos_3=2714-start

pause_time= 0.5 # Pause time for loop in seconds
daq_time =5     # Data acquisition time (s)

while_end=3
while_counter=0
#------------ PREPARE INITIAL DATA-------------------
data_tracking=list()
data_btracking=list()
data_setp=list()
time_list=list()

while len(data_tracking)<1 or while_counter<while_end:
    try:
        plc.connect(plc_addr,0,1,tcpport)
        mbyte = plc.read_area(area,db_number,start,length)
        data_tracking.append(snap7.util.get_real(mbyte,pos_1))
        data_btracking.append(snap7.util.get_real(mbyte,pos_2))
        data_setp.append(snap7.util.get_real(mbyte,pos_3))
        time_list.append(0)
        plc.disconnect()
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
plt.ylabel('Angle (deg)')
plt.plot(time_list,data_tracking,c='b',label='Pos. 1')
plt.plot(time_list,data_btracking,c='r',label='Pos. 2')
plt.plot(time_list,data_setp,c='g',label='Pos. 3')
plt.legend(loc=1)
plt.grid(linestyle='-')
plt.title('Monitoring S7 calculation')

print('Initialisation done! - Starting DAQ!')
#------------ START DAQ LOOP-------------------
for i in range(int(rng)):

    while while_counter<while_end:
        try:
            plc.connect(plc_addr,0,1,tcpport)
            mbyte = plc.read_area(area,db_number,start,length)
            plc.disconnect()
            
            value_tr=snap7.util.get_real(mbyte,pos_1)
            value_btr=snap7.util.get_real(mbyte,pos_2)
            value_sp=snap7.util.get_real(mbyte,pos_3)
            
            data_tracking.append(value_tr)
            data_btracking.append(value_btr)
            data_setp.append(value_sp)
            time_list.append((i+1)*pause_time)
                        
            plt.plot(time_list[-2:],data_tracking[-2:],c='b',linewidth=1)
            plt.plot(time_list[-2:],data_btracking[-2:],c='r',linewidth=1)
            plt.plot(time_list[-2:],data_setp[-2:],c='g',linewidth=1)
            
            plt.show()
            plt.pause(pause_time)
            
        except:
            print('Exception raised in DAQ')
            while_counter=while_counter+1
            continue
        break

plt.show()
print("PLC connected: ",plc.get_connected())
end_time=t.time()
total_time=end_time-start_time
print("END - ","Time taken: ", total_time," sec")