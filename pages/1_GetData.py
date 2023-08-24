import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import DB
import re
import db_layout as layouts
import plotly.express as px
import pandas as pd
from db_layout import *
from utils import get_att
from datetime import datetime
import time
import os
import json
import csv

# Streamlit configuration settings
st.set_page_config(
    page_title="Data Acquisition",
    page_icon=r"favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    })


# Initialize session_state
if "temp" not in st.session_state:
    st.session_state["temp"] = False

# Display header
st.header('Testing')

# Database setup
dblist = [elem for elem in dir(layouts) if "__" not in elem]
db_nums = np.array([int(re.findall(pattern=r'\d+', string=db)[0]) for db in dblist])
dbdict = {num: dbs for num, dbs in zip(db_nums, dblist)}

st.session_state["dblist_arr"] = np.array(dblist)
testname = st.text_input("Testname:", value="Test_name")

if "db" not in st.session_state:
    st.session_state["db"] = DB.DB()

db = st.session_state["db"]
db.db_number = st.selectbox("Select Database to read from", db_nums)
db.layout = eval(dbdict[db.db_number])
db.layout_dict, dt_dict, db.param_datetype = get_att(db.layout)
db.dt_dict = dt_dict

# Select parameters
params = np.array([vals for vals in db.layout_dict.values()])
selected_params = st.multiselect("Select Params to track", params)

if "tracking_params" not in st.session_state:
    st.session_state["tracking_params"] = []

if selected_params:
    db.keys = selected_params
    db.temp_dict.update({k: [] for k in db.keys if k not in db.temp_dict.keys()})
    st.session_state["tracking_params"] = selected_params
selected_params = st.session_state["tracking_params"]
ip = st.text_input("Put in the IP:", value="192.168.29.152")
db.ip = str(ip)
db.keys = selected_params

if "times" not in st.session_state:
    st.session_state["times"] = []

if "test_name" not in st.session_state:
    st.session_state["test_name"] = ""

# Select plots and values
selected_plots = st.multiselect("Select Plots to Show", st.session_state["tracking_params"], key="sp")
selected_values = st.multiselect("Select Values to Show", st.session_state["tracking_params"], key="sv")

# Initialize database setup
def init_setup():
    st.session_state["db"].set_up()
st.write(st.session_state["db"].plc)

# Set test name and initiate setup
st.session_state["test_name"] = testname
if st.checkbox('Connect', key="con") and st.session_state["temp"] == False:
    init_setup()

# Initialize DataFrame for tracking
if "df" not in st.session_state:
    data = pd.DataFrame(columns=['times'] + selected_params)
    st.session_state["df"] = data

# Display title
st.title(f"Tracking DB: {db.db_number} at IP: {db.ip}")

# Initialize plot
if "fig" not in st.session_state:
    fig, ax = plt.subplots()
    ax.relim()
    st.session_state["fig"] = fig
    st.session_state["ax"] = ax
else:
    fig = st.session_state["fig"]
    ax = st.session_state["ax"]

line, = ax.plot([], [])

# Save button
save_button = st.button("Save", key="save_data")

# Function to save data
def onClickFunction(name):
    data_dict = {
        "testname": st.session_state["test_name"],
        "Date": datetime.timestamp(datetime.now()),
        "parameters": st.session_state["tracking_params"],
        "ip": db.ip,
        "DB-Number": f"{db.db_number}"
    }
    db.save_params(name, data_dict)

st.session_state["db"] = db

placeholder = st.empty()

path = "csv_data"
filenamecsv = st.session_state["test_name"] + ".csv"
filenamejson = st.session_state["test_name"] + ".json"


max_attempts = 10
n = 0
current_time = time.time()

if selected_params and st.session_state["con"]:
    if "init" not in st.session_state:
        if not os.path.isfile(os.path.join(path, filenamecsv)):
            db.temp_dict["times"] = []
            with open(os.path.join(path, filenamecsv), 'w') as f:
                print("created new file")
                w = csv.DictWriter(f, db.temp_dict.keys())
                w.writeheader()
            data_dict = {
                "testname": st.session_state["test_name"],
                "Date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time)),
                "parameters": st.session_state["tracking_params"],
                "ip": db.ip,
                "DB-Number": f"{db.db_number}"
            }

            with open(os.path.join(path, filenamejson), 'w') as json_file:
                json.dump(data_dict, json_file, indent=4)

            
        different_button = st.download_button(
            label="Download data as CSV",
            data=pd.read_csv(os.path.join(path,filenamecsv)).to_csv(),
            file_name=st.session_state["test_name"] + '.csv',
            mime='text/csv',
            key="Another One"
        )
    st.session_state["temp"] = True
    while True:
        try:
            with placeholder.container():
                n += 1
                if n % 5 == 0:
                    db.temp_dict = {key: [] for key in db.temp_dict.keys()}
                    db.times = []
                    
                db.get_data()
                db.temp_dict["times"] = db.times
                last_data = {key: value[-1] for key , value in db.temp_dict.items() if value}
                
                with open(os.path.join(path, filenamecsv), 'a', newline='') as f:
                    w = csv.DictWriter(f, db.temp_dict.keys())
                    w.writerow(last_data)

                if st.session_state["sv"]:
                    kpi_columns = st.columns(len(selected_values))
                    for i, param in enumerate(selected_values):
                        kpi_columns[i].metric(
                            label=param,
                            value=db.temp_dict[param][-1],
                        )

                if st.session_state["sp"]:
                    num_plots = len(selected_plots)
                    num_columns = 4
                    fig_columns = st.columns(num_columns)

                    for i, param in enumerate(selected_plots):
                        with fig_columns[i % num_columns]:
                            st.markdown(f"### {param}")
                            fig = px.line(data_frame=pd.read_csv(f'{path}/{filenamecsv}'), x="times", y=param)
                            st.plotly_chart(fig)

                st.write(db.times[-1])

                if save_button:
                    onClickFunction(testname)
                    save_button = False
                    print(st.session_state)
                if n %10 == 0:
                    max_attempts = 10

        except Exception as e:
            try:
                    db.set_up()
                    print(e)
            except Exception as f:
                with st.spinner('Reconnecting'):
                    print(max_attempts)

                    time.sleep(2)
                max_attempts -= 1
                if max_attempts <= 0:
                    st.warning("Too many attemps, stopped loop!")
                    break


                    


