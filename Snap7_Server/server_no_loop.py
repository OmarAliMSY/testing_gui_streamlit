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


layout="""
0   para1   REAL
4   para2   REAL
8   para3   REAL
"""
length=20

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

tcpport = 1102

server = snap7.server.Server()
size = 100*8
DBdata = (snap7.snap7types.wordlen_to_ctypes[snap7.snap7types.S7WLByte] * size)()
PAdata = (snap7.snap7types.wordlen_to_ctypes[snap7.snap7types.S7WLByte] * size)()
PEdata = (snap7.snap7types.wordlen_to_ctypes[snap7.snap7types.S7WLByte] * size)()
MKdata = (snap7.snap7types.wordlen_to_ctypes[snap7.snap7types.S7WLByte] * size)()
    
server.register_area(snap7.snap7types.srvAreaDB, 1, DBdata)

server.register_area(snap7.snap7types.srvAreaPA, 1, PAdata)
server.register_area(snap7.snap7types.srvAreaPE, 1, PEdata)
server.register_area(snap7.snap7types.srvAreaMK, 1, MKdata)
    
    

server.start(tcpport=tcpport)

snap7.util.set_real(DBdata,0,1.0)
snap7.util.set_real(PAdata,0,2.234)
snap7.util.set_real(PEdata,0,3.234)
snap7.util.set_real(MKdata,0,4.234)

db1=snap7.util.DB(1,DBdata,layout,length,1,layout_offset=0,db_offset=0)

db1[0]['para1']=2.0