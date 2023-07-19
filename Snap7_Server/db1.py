import time
from datetime import datetime as dt
import csv
import snap7
from snap7 import util


class DB:
    """
    Class representing a database.

    Attributes:
    - ip (str): IP address of the database.
    - db_number (int): Database number.
    - layout (str): Database layout.
    - temp_dict (dict): Dictionary to store temporary data.
    - data_types (dict): Dictionary mapping data type names to their code lengths.
    """

    data_types = {"USINT": 1, "BOOL": 2, "REAL": 4, "DTL": 12, "INT": 2}

    def __init__(self):
        self.ip = None
        self.db_number = None
        self.layout = None
        self.temp_dict = {}

    def set_connection(self, ip, db_number):
        """
        Set the IP address and database number for the connection.

        Args:
        - ip (str): IP address of the database.
        - db_number (int): Database number.
        """
        self.ip = ip
        self.db_number = db_number

    def set_layout(self, layout):
        """
        Set the database layout.

        Args:
        - layout (str): Database layout.
        """
        self.layout = layout

    def get_data(self, keys, interval, t):
        """
        Retrieve data from the database.

        Args:
        - keys (list): List of keys to retrieve data for.
        - interval (float): Time interval between data retrievals.
        - t (int): Number of data retrievals.

        Returns:
        - None
        """
        temp_dict = {k: [] for k in keys}
        print(f'Connecting to: {self.ip}')
        row_size = int(list(self.layout_dict.keys())[-1]) - int(list(self.layout_dict.keys())[0]) + self.data_types[
            self.dt_dict[int(list(self.layout_dict.keys())[-1])]]
        dbsize = row_size + self.data_types[
            self.dt_dict[int(list(self.layout_dict.keys())[-1])]]
        print(dbsize)
        plc = snap7.client.Client()
        plc.connect(self.ip, 0, 1)
        all_data1 = plc.db_read(self.db_number, 0, dbsize)

        db110 = util.DB(db_number=self.db_number, bytearray_=all_data1,
                        specification=self.layout, row_size=row_size, size=1,
                        layout_offset=int(list(self.layout_dict.keys())[0]),
                        db_offset=int(list(self.layout_dict.keys())[0]))

        for i in range(t):
            db110.read(plc)
            print(i)
            for key in keys:
                print(f'{key}:{db110[0][key]}')
                temp_dict[key].append(db110[0][key])
            time.sleep(interval)
        self.temp_dict = temp_dict

    def save_params(self):
        """
        Save the retrieved parameters to a CSV file.

        Returns:
        - None
        """
        date = dt.today().strftime('%Y-%m-%d')

        with open(date + '.csv', 'w') as f:
            w = csv.DictWriter(f, self.temp_dict.keys())
            w.writeheader()
            w.writerow(self.temp_dict)
