from DB import DB
from utils import get_att
from db_layout import *
import numpy as np
from datetime import datetime
import os
import csv 
import json
import time

db103 = DB()
db103.db_number = 103
db103.layout = layout_db103
db103.layout_dict, db103.dt_dict, db103.param_datetype = get_att(layout_db103)
db103.ip = "192.168.29.102"
params = np.array([vals for vals in db103.layout_dict.values()])
db103.keys = params
db103.temp_dict.update({k: [] for k in db103.keys if k not in db103.temp_dict.keys()})
db103.temp_dict.update({"times" : []})
db103.set_up()
i = 0
data_dict = {"testname": "Test_Lorem", "Date": datetime.timestamp(datetime.now()), 
             "parameters": f"{db103.keys}",
             "ip": db103.ip,
             "DB-Number": f"{db103.db_number}"}
data_dict["testname"] = input("Put Testname in: ")
path = r"csv_data"
filenamecsv = data_dict["testname"] + ".csv"
filenamejson = data_dict["testname"] + ".json"

# Check if the CSV file exists and write the header only if it's a new file
if not os.path.isfile(os.path.join(path, filenamecsv)):
    with open(os.path.join(path, filenamecsv), 'w') as f:
        print("created new file")
        w = csv.DictWriter(f, db103.temp_dict.keys())
        w.writeheader()

with open(os.path.join(path, filenamejson), 'w') as json_file:
    json.dump(data_dict, json_file, indent=4)  # 'indent=4' is op1tional for pretty formatting
max_attempts = 10
while True:
    try:
        print(db103.temp_dict)
        db103.get_data()
        i += 1
        db103.temp_dict["times"]  = db103.times
        # Create a new dictionary with the last values of each key
        last_data = {key: value[-1] for key, value in db103.temp_dict.items()}

        if i % 5 == 0:
            db103.temp_dict = {key: [] for key in db103.temp_dict.keys()}
            db103.times = []
            max_attempts = 10
        # Write the last data row to the CSV file
        with open(os.path.join(path, filenamecsv), 'a', newline='') as f:
            w = csv.DictWriter(f, db103.temp_dict.keys())
            w.writerow(last_data)


    except Exception as e:
        try:
            if max_attempts > 0:
                db103.set_up()
                max_attempts -= 1
                time.sleep(1)       # Delay before retrying
                continue
        except Exception as f:
            time.sleep(1)
            max_attempts -= 1
            continue
        else:
            print(f'Failed to connect to the database after multiple attempts Time: {db103.times}.')
            break