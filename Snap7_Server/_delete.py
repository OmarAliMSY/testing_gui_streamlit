# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 15:02:43 2019

@author: misa
"""
import snap7

plc=snap7.client.Client()
plc.connect('10.49.61.85',0,1,1102)



alldata=plc.db_read(511,0,1500)

val1=snap7.util.get_usint(alldata,0)
val2=snap7.util.get_int(alldata,2)
print(val1)
print(val2)


