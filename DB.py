import json
import time
import snap7
from Snap7_Server.db_layout import *
from snap7 import util
import csv
from datetime import datetime as dt


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
        self.temp_dict = {}
        self.layout = None
        self.layout_dict = {}
        self.db_number = None
        self.dt_dict = {}
        self.data_types = {"USINT": 1, "BOOL": 2, "REAL": 4, "DTL": 12, "INT": 2}
        self.keys = None
        self.plc = None
        self.db  = None
        self.temp_dict = None
    def set_up(self):

        self.temp_dict = {k: [] for k in self.keys}
        print(f'Connecting to: {self.ip,self.db_number}')
        row_size = int(list(self.layout_dict.keys())[-1]) - int(list(self.layout_dict.keys())[0]) + self.data_types[
            self.dt_dict[int(list(self.layout_dict.keys())[-1])]]
        size = int(list(self.layout_dict.keys())[-1]) + self.data_types[
            self.dt_dict[int(list(self.layout_dict.keys())[-1])]]

        self.plc = snap7.client.Client()
        self.plc.connect(self.ip, 0, 1)
        all_data1 = self.plc.db_read(self.db_number, 0, 128)

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
        print(self.layout_dict)
        self.db.read(self.plc)

        for key in self.keys:
            print(f'{key}: {self.db[0][key]}')
            self.temp_dict[key].append(self.db[0][key])
        time.sleep(1)
        self.temp_dict = self.temp_dict


    def save_params(self,name):
        """
        Save parameters to a CSV file with the current date as the filename.
        """
        date = dt.today().strftime('%Y-%m-%d')

        with open(name +date + '.csv', 'w') as f:
            w = csv.DictWriter(f, self.temp_dict.keys())
            w.writeheader()
            w.writerow(self.temp_dict)
