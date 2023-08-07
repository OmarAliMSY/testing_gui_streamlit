from DB import DB
from utils import get_att
from db_layout import *
import numpy as np

db103 = DB()
db103.db_number = 103
db103.layout = layout_db103
db103.layout_dict, db103.dt_dict,db103.param_datetype = get_att(layout_db103)
db103.ip = "192.168.29.102"
params = np.array([vals for vals in db103.layout_dict.values()])
db103.keys = params
db103.temp_dict.update({k: [] for k in db103.keys if k not in db103.temp_dict.keys()})
db103.set_up()
i = 0

while True:
    try:
        print(i)
        db103.get_data()
        i+=1
    except Exception as e:
        print("Failed because of " ,e)