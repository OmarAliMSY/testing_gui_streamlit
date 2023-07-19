from time import sleep
import snap7
from snap7.util import *

plc = snap7.client.Client()
plc.connect('10.49.61.85',0,1,1103)
area1 = 0x83 # srvAreaMK
area2 = 0x82 # srvAreaPA
area3 = 0x81 # srvAreaPE
area4 = 0x84 # srvAreaDB
start = 0
length = 4
float1=plc.read_area(area1,1,start,length)
float2=plc.read_area(area2,1,start,length)
float3=plc.read_area(area3,1,start,length)
float4=plc.read_area(area4,1,start,length)

print("Area=MK, [0,4]={}".format(get_real(float1,0)))
print("Area=PA, [0,4]={}".format(get_real(float2,0)))
print("Area=PE, [0,4]={}".format(get_real(float3,0)))
print("Area=DB, [0,4]={}".format(get_real(float4,0)))

plc.disconnect()