from DB import DB
from utils.utils import get_att
from utils.db_layout import *
import utils.db_layout as layouts
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

# Define a function to flatten and combine keys from liTorsts of NumPy arrays
def combine_keys(keys_list):
    flattened_keys = [key for keys in keys_list for key in keys]
    return list(set(flattened_keys))  # Use set to remove duplicates

configlist = [{"db_layout" :layout_db103,"ip":"192.168.29.150","db_number":103}
              ,{"db_layout" :layout_db105,"ip":"192.168.29.150","db_number":105}]

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
dbs = [setup_db(configs) for configs in configlist]



data_dict = {"testname": "Test_Lorem", "Date": datetime.timestamp(datetime.now()), 
                "parameters": f"{dbs[0].keys}",
                "ip": dbs[0].ip,
                "DB-Number": f"{dbs[0].db_number}"}

data_dict["testname"] = input("Put Testname in: ")
if dbs:
    data_dict["parameters"] = [a.keys for a in dbs]
    data_dict["ip"] = [a.ip for a in dbs]
    data_dict["DB-Number"] = [a.db_number for a in dbs]

path = r"csv_data\torque_tests"
filenamecsv = data_dict["testname"] + ".csv"
filenamejson = data_dict["testname"] + ".json"



if not os.path.isfile(os.path.join(path, filenamecsv)):
    with open(os.path.join(path, filenamecsv), 'w') as f:
        print("created new file")
        combined_keys = combine_keys([list(db.temp_dict.keys()) for db in dbs])  # Combine keys
        w = csv.DictWriter(f, combined_keys)
        w.writeheader()
    with open(os.path.join(path, filenamejson), 'w') as json_file:
        json.dump(convert_numpy_arrays(data_dict), json_file, indent=4)  # Convert NumPy arrays to lists

# Converting numpy arrays in all dbs
for db in dbs:
    db.temp_dict = convert_numpy_arrays(db.temp_dict)

# Function to merge temp_dicts from all dbs
def merge_temp_dicts(dbs):
    merged_dict = {}
    for db in dbs:
        for key, value in db.temp_dict.items():
            if key not in merged_dict:
                merged_dict[key] = value
            else:
                merged_dict[key].extend(value)
    return merged_dict

max_attempts = 10
i = 0

while True:
    try:
        for db in dbs:
            db.get_data()
            db.temp_dict["times"] = db.times

        # Merging temp_dicts and times from all dbs
        merged_temp_dict = merge_temp_dicts(dbs)

        i += 1

        if i % 5 == 0:
            for db in dbs:
                db.temp_dict = {key: [] for key in db.temp_dict.keys()}
                db.times = []
            max_attempts = 10

        # Write the last data row to the CSV file
        with open(os.path.join(path, filenamecsv), 'a', newline='') as f:
            w = csv.DictWriter(f, combined_keys)  # Use combined parameters
            # Extracting last values from merged_temp_dict
            last_data = {key: value[-1] if value else None for key, value in merged_temp_dict.items()}
            w.writerow(last_data)

    except Exception as e:
        try:
            if max_attempts > 0:
                # Re-setup all dbs
                for db in dbs:
                    db.set_up()
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