#!/usr/bin/env python
"""
This is an example snap7 server. It doesn't do much, but accepts
connection. Useful for running the python-snap7 test suite.
"""
import time
import logging
import snap7
import sys
import numpy as np
from db_layout import layout_db110 as layout_db110
from db_layout import layout_db504_tr as layout_db504_tr
#from db_layout import layout_db504_f as layout_db504_f
from db_layout import layout_db511 as layout_db511
from db_layout import POS_LASTSETPOINT as POS_LASTSETPOINT
from db_layout import POS_CURRENTANGLE as POS_CURRENTANGLE
from db_layout import POS_DELTAPHI as POS_DELTAPHI
from db_layout import POS_DAYMAXANGLE as POS_DAYMAXANGLE
from db_layout import POS_DAYMINANGLE as POS_DAYMINANGLE
from db_layout import POS_MAXLASTMOTORCURRENT as POS_MAXLASTMOTORCURRENT
from db_layout import POS_MAXLASTMOTORTORQUE as POS_MAXLASTMOTORTORQUE

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

tcpport_start = 102        # Start of tcp port number for dummy server (tcpport_start+num_fields is tcp port of last server)
num_fields=1                # number of dummy fields to generate
num_trackers=31             # number of trackers per field
loop_sleep_time=1         # mainloop() loop sleep time in seconds

db110_size = 3668              # size of db to be simulated per field
db504_size = 2290
db511_size = 1500

server_obj_list=[]          # server obejcts can be accesed via index number server_obj_list[i]

DB110data_obj_list=[]       # DB110data obejcts can be accesed via index number DB110data_obj_list[i] - direct access via byte index
db110_obj_list=[]           # db obejcts can be accesed via index number db110_obj_list[i][param_name] - direct access via byte index & param name from layout

DB504data_obj_list=[]
db504_tr_obj_list=[]

DB511data_obj_list=[]
db511_obj_list=[]



def mainloop():           
                
    for a in range(num_fields):
        server = snap7.server.Server()
        server_obj_list.append(server)
        
        DB110data = (snap7.types.wordlen_to_ctypes[snap7.types.S7WLByte] * db110_size)()
        DB110data_obj_list.append(DB110data)
        DB504data = (snap7.types.wordlen_to_ctypes[snap7.types.S7WLByte] * db504_size)()
        DB504data_obj_list.append(DB504data)
        DB511data = (snap7.types.wordlen_to_ctypes[snap7.types.S7WLByte] * db511_size)()
        DB511data_obj_list.append(DB511data)
        
        server_obj_list[a].start(tcpport=tcpport_start+a)
        server_obj_list[a].register_area(snap7.types.srvAreaDB, 110, DB110data_obj_list[a])
        server_obj_list[a].register_area(snap7.types.srvAreaDB, 504, DB504data_obj_list[a])
        server_obj_list[a].register_area(snap7.types.srvAreaDB, 511, DB511data_obj_list[a])
        
        db110=snap7.util.DB(110,DB110data_obj_list[a],layout_db110,80,num_trackers,layout_offset=82,db_offset=82)
        db110_obj_list.append(db110)
        
        db504_tr=snap7.util.DB(504,DB504data_obj_list[a],layout_db504_tr,72,num_trackers,layout_offset=0,db_offset=0)
        db504_tr_obj_list.append(db504_tr)

        db511=snap7.util.DB(110,DB511data_obj_list[a],layout_db511,16,(31*3),layout_offset=0,db_offset=0)
        db511_obj_list.append(db511)
        
        print('***MISA: Server & DB objects created!')
          
    while True:
                
        for num_field in range(num_fields):
            
            gen_field_data(num_field,num_trackers)
        
        while True:
            event = server.pick_event()
            if event:
                logger.info(server.event_text(event))
            else:
                break
        time.sleep(loop_sleep_time)





def gen_field_data(n_field,n_trackers):
    
    i = np.sin(2*np.pi*(1/10)*time.time())        # sin wave amplitude = 1; frequency = 0.1 Hz
    i_bool = i > 0                                  # boolean with switching frequency = 0.1 Hz
    j = np.cos(2*np.pi*(1/10)*time.time())        # cos wave amplitude = 1; frequency = 0.1 Hz
    
    #DB504 field errors
    for err in range(3):
        snap7.util.set_usint(DB504data_obj_list[n_field], 2232+err*16, 1 )
        snap7.util.set_usint(DB504data_obj_list[n_field], 2233+err*16, 1 )
        #snap7.util.set_dtl(DB504data_obj_list[n_field], 2232+i*16, 1 )
        snap7.util.set_int(DB504data_obj_list[n_field], 2246+err*16, 4*i_bool )
    
    for event in range(31*3):
        db511_obj_list[n_field][event]['tr_adress']=int(2)*7
        db511_obj_list[n_field][event]['errorcode']=int(3)*8
        
        
    for n_tr in range(n_trackers):
        
        # DB110 Tracker data generation
        db110_obj_list[n_field][n_tr]['SetFrequ']    =   50+i
        db110_obj_list[n_field][n_tr]['ActFrequ']    =   50-i
        db110_obj_list[n_field][n_tr]['phi1']        =   10*i+(n_tr+1)*10
        db110_obj_list[n_field][n_tr]['phi2']        =   10*j+(n_tr+1)*10
        db110_obj_list[n_field][n_tr]['twist_angle'] =   i-j
        db110_obj_list[n_field][n_tr]['nSoftOM']     =   211
        #db110_obj_list[n_field][n_tr]['local']       =   i_bool
        db110_obj_list[n_field][n_tr]['STW1']        =   12+int(i_bool)
        db110_obj_list[n_field][n_tr]['STW2']        =   127+int(i_bool)
        db110_obj_list[n_field][n_tr]['Torque']        =   31
        
        #                    DBobject[index]            Data location                       Simulated value
        snap7.util.set_real(DB110data_obj_list[n_field],   POS_LASTSETPOINT+4*n_tr ,           10*i+(n_tr+1)*10    )
        snap7.util.set_real(DB110data_obj_list[n_field],   POS_CURRENTANGLE+4*n_tr,            10*j+(n_tr+1)*10    )
        snap7.util.set_real(DB110data_obj_list[n_field],   POS_DELTAPHI+4*n_tr,                1*i+(n_tr+1)        )
        snap7.util.set_real(DB110data_obj_list[n_field],   POS_DAYMAXANGLE+4*n_tr,             40+i                )
        snap7.util.set_real(DB110data_obj_list[n_field],   POS_DAYMINANGLE+4*n_tr,             -40-j               )
        snap7.util.set_real(DB110data_obj_list[n_field],   POS_MAXLASTMOTORCURRENT+4*n_tr,     1*i+(n_tr+1)*10     )
        snap7.util.set_real(DB110data_obj_list[n_field],   POS_MAXLASTMOTORTORQUE+4*n_tr,      1*i+(n_tr+1)*10     )
        
        # DB504
        
        for n_err in range(3):
            db504_tr_obj_list[n_field][n_tr]['wz_adress_'+str(n_err+1)] = 11
            db504_tr_obj_list[n_field][n_tr]['tr_adress_'+str(n_err+1)] = n_tr
            db504_tr_obj_list[n_field][n_tr]['errorcode_'+str(n_err+1)] = 5
            #db504_tr_obj_list[n_field][n_tr]['timestamp_' + str(n_err + 1)] = time.time()
            
         
        
    
    
    
if __name__ == '__main__':
    if len(sys.argv) > 1:
        snap7.common.load_library(sys.argv[1])
    mainloop()