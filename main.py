import numpy as np  # np mean, np random
import matplotlib.pyplot as plt
import streamlit as st  # 🎈 data web app development
import DB
import re
import db_layout as layouts
import plotly.express as px
import pandas as pd
from db_layout import *
from utils import get_att
from datetime import datetime

st.set_page_config(
    page_title="Data aquisition",
    page_icon=r"favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    })


if "temp" not in st.session_state:
    st.session_state["temp"] = False


st.header('Testing')

dblist = [elem for elem in dir(layouts) if "__" not in elem]
db_nums = np.array([int(re.findall(pattern=r'\d+', string=db)[0]) for db in dblist])
dbdict = {num : dbs for num,dbs in zip(db_nums,dblist)}

st.session_state["dblist_arr"] = np.array(dblist)
testname = st.text_input("Testname:",value="Test_name")


if "db" not in st.session_state:
    st.session_state["db"] = DB.DB()
db = st.session_state["db"]
db.db_number  = st.selectbox("Select Database to read from", db_nums)
db = st.session_state["db"] 
db.layout = eval(dbdict[db.db_number] )
db.layout_dict, dt_dict,db.param_datetype = get_att(db.layout)
db.dt_dict = dt_dict

params = np.array([vals for vals in db.layout_dict.values()])
selected_params = st.multiselect("Select Params to track",params)

if "tracking_params" not in st.session_state:
        st.session_state["tracking_params"]  = []

if selected_params:
    db.keys = selected_params
    db.temp_dict.update({k: [] for k in db.keys if k not in db.temp_dict.keys()})
    st.session_state["tracking_params"] = selected_params

ip = st.text_input("Put in the IP:",value="192.168.29.152")
db.ip = str(ip)
db.keys = selected_params

if "times" not in st.session_state:
    st.session_state["times"] = []

if "test_name" not in st.session_state:
    st.session_state["test_name"] = ""
    
selected_plots = st.multiselect("Select Plots to Show", selected_params,key="sp")
selected_values = st.multiselect("Select Values to Show", selected_params,key="sv")

def init_setup():
        st.session_state["db"].set_up()

st.session_state["test_name"] = testname
if st.checkbox('Connect',key="con") and st.session_state["temp"] == False:
    init_setup()
    

if "df" not in st.session_state:
    data = pd.DataFrame(columns=['times'] + selected_params) 
    st.session_state["df"] = data

st.title(f"Tracking DB: {db.db_number }")

if "fig" not in st.session_state:
    fig, ax = plt.subplots()
    ax.relim()
    st.session_state["fig"] = fig
    st.session_state["ax"] = ax

else:
    fig = st.session_state["fig"]
    ax = st.session_state["ax"]

line, = ax.plot([], [])


save_button = st.button("Save",key="save_data")

def onClickFunction(name):
    data_dict = {"testname" : st.session_state["test_name"],"Date": datetime.timestamp(datetime.now()), 
                 "parameters" : st.session_state["tracking_params"],
                 "ip" : db.ip,
                 "DB-Number" : f"{db.db_number }"}

    db.save_params(name,data_dict)
   
st.session_state["db"] = db

placeholder = st.empty()

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(st.session_state["df"])

different_button = st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name=st.session_state["test_name"]+'.csv',
    mime='text/csv',
    key="Another One"
)

if selected_params and st.session_state["con"]:
        st.session_state["temp"]  = True
        while True:
            with placeholder.container():
                db.get_data()

                data = pd.DataFrame(
                {'times': db.times, **{param: db.temp_dict[param] for param in selected_params}})
                data.set_index("times")

                st.session_state["df"] = data

                if selected_values:
                    kpi_columns = st.columns(len(selected_values))
                    for i, param in enumerate(selected_values):
                        kpi_columns[i].metric(
                            label=param,
                            
                            value=db.temp_dict[param][-1],
                        )

                if selected_plots:
                    num_plots = len(selected_plots)
                    num_columns = 4
                    fig_columns = st.columns(num_columns)

                    for i, param in enumerate(selected_plots):
                        with fig_columns[i % num_columns]:  
                            st.markdown(f"### {param}")
                            fig = px.line(data_frame=data, x="times", y=param)
                            st.write(fig)
                st.write(db.times[-1])
            if save_button:
                onClickFunction(testname)
                
                save_button = False
                print(st.session_state)