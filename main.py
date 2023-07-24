import time  # to simulate a real time data, time loop
import numpy as np  # np mean, np random
import matplotlib.pyplot as plt
import streamlit as st  # 🎈 data web app development
import DB
import re
import db_layout as layouts
import plotly.express as px
import pandas as pd
from db_layout import *


st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    })

st.header('DAQ')

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
    print(db_dict,db_dt)
    param_datetype = {row[1]: row[2] for row in item_list}
    return db_dt, db_dict,param_datetype


dblist = [elem for elem in dir(layouts) if "__" not in elem]

db_nums = np.array([int(re.findall(pattern=r'\d+', string=db)[0]) for db in dblist])

dbdict = {num : dbs for num,dbs in zip(db_nums,dblist)}

st.session_state["dblist_arr"] = np.array(dblist)
select_db = st.selectbox("Select Database to read from", db_nums)
db = DB.DB()
st.session_state["db"] = db

layout = eval(dbdict[select_db] )
dictionary, dt_dict,db.param_datetype = get_att(layout)
db.layout = layout
db.layout_dict = dictionary
db.db_number = select_db
#db.db_number = int(re.findall(pattern=r'\d+', string=select_db )[0])
db.dt_dict = dt_dict
params = np.array([vals for vals in dictionary.values()])
selected_params = st.multiselect("Select Params to track",params)
ip = st.text_input("Put in the IP:",value="192.168.29.152")
db.ip = str(ip)
db.keys = selected_params

if "times" not in st.session_state:
    st.session_state["times"] = []



# Multiselect box to select plots
selected_plots = st.multiselect("Select Plots to Show", selected_params,key="sp")

# Multiselect box to select values
selected_values = st.multiselect("Select Values to Show", selected_params,key="sv")
if st.checkbox('Connect',key="con"):

    st.session_state["db"].set_up()
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

if "df" not in st.session_state:
    st.session_state["df"] = None

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

# Create an initial empty line


# creating a single-element container
placeholder = st.empty()


fig_col1, fig_col2 = st.columns(2)

if selected_params and st.session_state["con"]:
    #try:
        while True:
            with placeholder.container():
                st.session_state["db"].get_data()

                
                current_time = time.time()

                # Convert the Unix timestamp to a formatted time string
                formatted_time = time.strftime("%H:%M:%S", time.localtime(current_time))

                # Append the formatted time to the list
                st.session_state["times"].append(formatted_time)

                # Update the x-axis data with the new list of formatted times
                x_data= st.session_state["times"]
                data = pd.DataFrame(
                {'times': x_data, **{param: st.session_state["db"].temp_dict[param] for param in selected_params}})
                data.set_index("times")
                st.session_state["df"] = data

                if selected_values:

                # Display selected values
                    kpi_columns = st.columns(len(selected_values))
                    for i, param in enumerate(selected_values):
                        kpi_columns[i].metric(
                            label=param,
                            value=st.session_state["db"].temp_dict[param][-1],
                        )
                if selected_plots:
                    num_plots = len(selected_plots)
                    num_columns = 4
                    

                    fig_columns = st.columns(num_columns)

                    for i, param in enumerate(selected_plots):
                        with fig_columns[i % num_columns]:  # Ensure the plots are placed in the correct column
                            st.markdown(f"### {param}")
                            fig = px.line(data_frame=data, x="times", y=param)
                            st.write(fig)

                

                if st.session_state["df"] is not None:
                    current_time = time.time()

                    # Convert the Unix timestamp to a formatted time string
                    formatted_time = time.strftime("%H:%M:%S", time.localtime(current_time))
                    st.download_button(
                        label="Download data as CSV",
                        data=convert_df(st.session_state["df"]),
                        file_name=str(formatted_time)+".csv",
                        mime='text/csv',
                    )



    #except Exception as e:
    #    print(st.session_state)
    #    st.session_state["df"].to_csv('output.csv', index=False)
    #    print(e)


