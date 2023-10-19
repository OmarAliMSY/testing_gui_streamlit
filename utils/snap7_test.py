from DB import DB
from utils import get_att
from db_layout import *
import db_layout as layouts
import numpy as np
import snap7
import time

db_config_103 = {"db_layout" :layout_db103,"ip":"192.168.29.150","db_number":103}



client = snap7.client.Client()
client.connect("192.168.29.150", 0, 1)
all_data = client.db_read(103,0,184)
print(all_data)
db1 = snap7.util.DB(
    103,                                        # the db we use
    all_data,                                   # bytearray from the plc
    db_config_103["db_layout"],                 # layout specification DB variable data
                                                # A DB specification is the specification of a
                                                # DB object in the PLC you can find it using
                                                # the dataview option on a DB object in PCS
184,                                             # size of the specification 17 is start
                                                # of last value
                                                # which is a DWORD which is 2 bytes,

    1,                                          # number of row's / specifications

                                                # field we can use to identify a row.
                                                # default index is used
    layout_offset=82,                            # sometimes specification does not start a 0
                                                # like in our example
    db_offset=82                                 # At which point in 'all_data' should we start
                                                # reading. if could be that the specification
                                                # does not start at 0
)
print(db1[0])
for i in range(5):
    print(db1[0])
    time.sleep(1)
    