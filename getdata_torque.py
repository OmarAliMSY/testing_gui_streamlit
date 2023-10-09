from DB import DB
from utils import get_att
from db_layout import *
import db_layout as layouts
import numpy as np
from datetime import datetime
import os
import csv 
import json
import time


def convert_numpy_arrays(data_dict):
    for key, value in data_dict.items():
        if isinstance(value, np.ndarray):
            data_dict[key] = value.tolist()
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, np.ndarray):
                    value[i] = item.tolist()
    return data_dict

# Define a function to flatten and combine keys from lists of NumPy arrays
def combine_keys(keys_list):
    flattened_keys = [key for keys in keys_list for key in keys]
    return list(set(flattened_keys))  # Use set to remove duplicates

db_config_103 = {"db_layout" :layout_db103,"ip":"192.168.29.150","db_number":103,}
db_config_102 = {"db_layout" :layout_db102,"ip":"192.168.29.152","db_number":102}

def setup_db (db_config):
    db = DB()
    db.layout = db_config["db_layout"]
    db.layout_dict, db.dt_dict, db.param_datetype = get_att(db.layout)
    db.ip = db_config["ip"]
    db.db_number = db_config["db_number"]
    params = np.array([vals for vals in db.layout_dict.values()])
    db.keys = params
    db.temp_dict.update({k: [] for k in db.keys if k not in db.temp_dict.keys()})
    db.temp_dict.update({"times" : []})
    
  
    db.set_up()
    return db
db1 = setup_db(db_config_103)
db2 = setup_db(db_config_102)

dbs = [db1,db2]


data_dict = {"testname": "Test_Lorem", "Date": datetime.timestamp(datetime.now()), 
                "parameters": f"{db1.keys}",
                "ip": db1.ip,
                "DB-Number": f"{db1.db_number}"}

data_dict["testname"] = input("Put Testname in: ")
if dbs:
    data_dict["parameters"] = [a.keys for a in dbs]
    data_dict["ip"] = [a.ip for a in dbs]
    data_dict["DB-Number"] = [a.db_number for a in dbs]

path = r"csv_data"
filenamecsv = data_dict["testname"] + ".csv"
filenamejson = data_dict["testname"] + ".json"

# Check if the CSV file exists and write the header only if it's a new file
print(data_dict["parameters"],type(data_dict["parameters"]))
# Check if the CSV file exists and write the header only if it's a new file
if not os.path.isfile(os.path.join(path, filenamecsv)):
    with open(os.path.join(path, filenamecsv), 'w') as f:
        print("created new file")
        combined_keys = combine_keys([list(db.temp_dict.keys()) for db in [db1, db2]])  # Combine keys
        w = csv.DictWriter(f, combined_keys)
        w.writeheader()
    with open(os.path.join(path, filenamejson), 'w') as json_file:
        json.dump(convert_numpy_arrays(data_dict), json_file, indent=4)  # Convert NumPy arrays to lists

max_attempts = 10

i = 0
while True:
    try:
        db1.get_data()
        db2.get_data()

        i += 1
        db1.temp_dict["times"] = db1.times
        db2.temp_dict["times"] = db2.times

        # Create a new dictionary with the last values of each key from both databases
        last_data = {**convert_numpy_arrays({key: value[-1] for key, value in db1.temp_dict.items()}),
                     **convert_numpy_arrays({key: value[-1] for key, value in db2.temp_dict.items()})}


        if i % 5 == 0:
            db1.temp_dict = {key: [] for key in db1.temp_dict.keys()}
            db2.temp_dict = {key: [] for key in db2.temp_dict.keys()}
            db1.times = []
            db2.times = []
            max_attempts = 10

        # Write the last data row to the CSV file
        with open(os.path.join(r"csv_data", filenamecsv), 'a', newline='') as f:
            w = csv.DictWriter(f, combined_keys)  # Use combined parameters
            w.writerow(last_data)

    except Exception as e:
        try:
            if max_attempts > 0:
                db1.set_up()
                db2.set_up()
                max_attempts -= 1
                time.sleep(1)  # Delay before retrying
                continue
        except Exception as f:
            time.sleep(1)
            max_attempts -= 1
            continue
        else:
            print(f'Failed to connect to the databases after multiple attempts.')
            break
