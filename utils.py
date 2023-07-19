import DB
import re
import db_layout as layouts
from db_layout import *
import numpy as np

def get_att(dbb_layout):
    """
    Process the database layout and extract attributes.

    Args:
    - dbb_layout: String representing the database layout.

    Returns:
    - Tuple containing two dictionaries:
        - db_dt: Dictionary mapping database numbers to their corresponding layout names.
        - db_dict: Dictionary mapping database numbers to their corresponding layout attributes.
    """
    item_list = [x.strip().split() for x in dbb_layout.split("\n") if x.strip()]
    db_dict = {int(float(row[0])): row[2] for row in item_list}
    db_dt = {row[0]: row[1] for row in item_list}
    return db_dt, db_dict


db = DB.DB()
dblist = [elem for elem in dir(layouts) if "__" not in elem]
db_nums = [int(re.findall(pattern=r'\d+', string=db)[0]) for db in dblist]
selected_value = dblist[0]

layout = eval(selected_value)
print(layout)
dictionary, dt_dict = get_att(layout)

db.layout = layout
db.layout_dict = dictionary
db.db_number = int(re.findall(pattern=r'\d+', string=selected_value)[0])
db.dt_dict = dt_dict
params = np.array([vals for vals in dictionary.values()])
print(db.db_number)
print(params)
db.ip = "192.168.29.152"
db.keys = params
db.set_up()
