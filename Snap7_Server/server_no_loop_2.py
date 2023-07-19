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
from db_layout import layout_db504_f as layout_db504_f
from db_layout import layout_db511 as layout_db511
from db_layout import POS_LASTSETPOINT as POS_LASTSETPOINT
from db_layout import POS_CURRENTANGLE as POS_CURRENTANGLE
from db_layout import POS_DELTAPHI as POS_DELTAPHI
from db_layout import POS_DAYMAXANGLE as POS_DAYMAXANGLE
from db_layout import POS_DAYMINANGLE as POS_DAYMINANGLE
from db_layout import POS_MAXLASTMOTORCURRENT as POS_MAXLASTMOTORCURRENT
from db_layout import POS_MAXLASTMOTORTORQUE as POS_MAXLASTMOTORTORQUE


layout="""
0   para1   REAL
4   para2   REAL
8   para3   REAL
"""
length=20
db110_size = 3668              # size of db to be simulated per field
db504_size = 2290
db511_size = 1500

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

tcpport = 102

server = snap7.server.Server()
size = 100*8
DBdata = (snap7.snap7types.wordlen_to_ctypes[snap7.snap7types.S7WLByte] * size)()
DB110data = (snap7.snap7types.wordlen_to_ctypes[snap7.snap7types.S7WLByte] * db110_size)()
DB504data = (snap7.snap7types.wordlen_to_ctypes[snap7.snap7types.S7WLByte] * db504_size)()
DB511data = (snap7.snap7types.wordlen_to_ctypes[snap7.snap7types.S7WLByte] * db511_size)()
    
server.register_area(snap7.snap7types.srvAreaDB, 1, DBdata)
server.register_area(snap7.snap7types.srvAreaDB, 110, DB110data)
server.register_area(snap7.snap7types.srvAreaDB, 504, DB504data)
server.register_area(snap7.snap7types.srvAreaDB, 511, DB511data)
   

server.start(tcpport=tcpport)
server.unlock_area(snap7.snap7types.srvAreaDB,110)
server.unlock_area(snap7.snap7types.srvAreaDB,504)
server.unlock_area(snap7.snap7types.srvAreaDB,511)

db1=snap7.util.DB(1,DBdata,layout,length,1,layout_offset=0,db_offset=0)

db110=snap7.util.DB(110,DB110data,layout_db110,80,1,layout_offset=82,db_offset=82)

db504_tr=snap7.util.DB(504,DB504data,layout_db504_tr,72,1,layout_offset=0,db_offset=0)



        
db511=snap7.util.DB(110,DB511data,layout_db511,16,(31*3),layout_offset=0,db_offset=0)


db504_tr[0]['wz_adress_1']=1
db504_tr[0]['tr_adress_1']=2
db504_tr[0]['errorcode_1']=3
snap7.util.set_usint(DB504data,2232,7)

db511[0]['tr_adress']=17
db511[0]['errorcode']=15
