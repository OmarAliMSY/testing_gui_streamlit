import json
import time
import snap7
from Snap7_Server.db_layout import *
from snap7 import util
import csv
from datetime import datetime as dt
from utils import get_unique_filename
import os

class DB:
    """
    Class representing a database.

    Attributes:
    - ip (str): IP address of the database.
    - temp_dict (dict): Temporary dictionary to store data.
    - layout (str): Database layout.
    - layout_dict (dict): Dictionary representing the layout.
    - db_number (int): Database number.
    - dt_dict (dict): Dictionary mapping data types to their codes.
    - data_types (dict): Dictionary mapping data type names to their code lengths.
    """

    def __init__(self):
        self.ip = None
        self.layout = None
        self.layout_dict = {}
        self.db_number = None
        self.dt_dict = {}
        self.data_types = {"USINT": 1, "BOOL": 2, "REAL": 4, "DTL": 12, "INT": 2}
        self.keys = []
        self.plc = None
        self.db  = None
        self.temp_dict = {}
        self.param_datetype = None
        self.times = []
        self.temp_dict = {}



    def set_up(self):
        print("Setting up")
        
        print(f'Connecting to: {self.ip,self.db_number}')
        row_size = int(list(self.layout_dict.keys())[-1]) - int(list(self.layout_dict.keys())[0]) + self.data_types[
            self.dt_dict[int(list(self.layout_dict.keys())[-1])]]
        size = int(list(self.layout_dict.keys())[-1]) + self.data_types[
            self.dt_dict[int(list(self.layout_dict.keys())[-1])]]
        self.plc = snap7.client.Client()
        self.plc.connect(self.ip, 0, 1)
        self.db_number = int(self.db_number)
        all_data1 = self.plc.db_read(self.db_number, 0, size)
        self.db = util.DB(db_number=self.db_number, bytearray_=all_data1,
                        specification=self.layout, row_size=row_size, size=1,
                        layout_offset=int(list(self.layout_dict.keys())[0]),
                        db_offset=int(list(self.layout_dict.keys())[0]))
    def get_data(self):
        """
        Retrieve data from the database.

        Args:
        - keys (list): List of keys to retrieve data for.
        - interval (int): Time interval between data reads.
        - t (int): Number of data readings to perform.
        """
        self.db.read(self.plc)
        current_time = time.time()

        # Convert the Unix timestamp to a formatted time string
        formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time))


        # Append the formatted time to the list
        

        # Update the x-axis data with the new list of formatted times
        
        for key in self.keys:
            self.temp_dict[key].append(self.db[0][key])

        self.times.append(formatted_time)


        
        time.sleep(1)
        


    def save_params(self, name, meta_dict):
        """
        Save parameters to a CSV file with the current date as the filename.
        """
        date = dt.today().strftime('%Y-%m-%d')
        filenamecsv = get_unique_filename(name, date, data="csv")
        filenamejson = get_unique_filename(name, date, data="json")
        print(filenamecsv)
        path = r"C:\Users\o.abdulmalik\OneDrive - Mounting Systems\Freigegebene Dokumente - PM Projects\Development\TRK_2110_Linear_Actuator\05 Testing"
        with open(os.path.join(path,filenamecsv), 'w') as f:
            print("created new file")
            w = csv.DictWriter(f, self.temp_dict.keys())
            w.writeheader()
            w.writerow(self.temp_dict)

        with open(os.path.join(path,filenamejson), 'w') as json_file:
            json.dump(meta_dict, json_file, indent=4)  # 'indent=4' is optional for pretty formatting

