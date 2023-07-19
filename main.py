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
    page_title="Real-Time Data Science Dashboard",
    page_icon="✅",
    layout="wide",
)
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


dblist = [elem for elem in dir(layouts) if "__" not in elem]
db_nums = [int(re.findall(pattern=r'\d+', string=db)[0]) for db in dblist]

st.session_state["dblist_arr"] = np.array(dblist)
select_db = st.selectbox("Select Database to read from", st.session_state["dblist_arr"])
db = DB.DB()
st.session_state["db"] = db

layout = eval(select_db )
dictionary, dt_dict = get_att(layout)
db.layout = layout
db.layout_dict = dictionary

db.db_number = int(re.findall(pattern=r'\d+', string=select_db )[0])
db.dt_dict = dt_dict
params = np.array([vals for vals in dictionary.values()])
selected_params = st.multiselect("Select Params to track",params)
ip = st.text_input("Put in the IP:",placeholder="192.168.29.152")
db.ip = "192.168.29.152"
db.keys = selected_params
if st.checkbox('Connect',key="con"):
    st.session_state["db"] .set_up()

print(st.session_state)
t = st.select_slider("Select Time",options=np.arange(1,5000+1,1),value=100)
#start = st.radio("Start",options=["Yes","No"],index=1)
temp = 0


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

# ... Existing code ...

# creating a single-element container
placeholder = st.empty()


fig_col1, fig_col2 = st.columns(2)

# near real-time / live feed simulation
if selected_params and st.session_state["con"]:
    try:
        while True:
            with placeholder.container():
                st.session_state["db"].get_data()

                kpi1, kpi2, kpi3 ,kpi4= st.columns(4)

                kpi1.metric(
                    label="maxLastMotorTorque",
                    value=st.session_state["db"].temp_dict["maxLastMotorTorque"][-1],
                )

                kpi2.metric(
                    label="statusNumber",
                    value=st.session_state["db"].temp_dict["statusNumber"][-1],
                )

                kpi3.metric(
                    label="TiltTwistAngle",
                    value=st.session_state["db"].temp_dict["TiltTwistAngle"][-1],
                )
                kpi4.metric(
                    label="southSensorAngle",
                    value=st.session_state["db"].temp_dict["southSensorAngle"][-1],
                )

                x_data = np.linspace(
                    1,
                    len(st.session_state["db"].temp_dict["maxLastMotorTorque"]),
                    len(st.session_state["db"].temp_dict["maxLastMotorTorque"]),
                        )

                data = pd.DataFrame(
                {'x_column': x_data, **{param: st.session_state["db"].temp_dict[param] for param in selected_params}})

                st.session_state["df"] = data

                fig_col1, fig_col2 = st.columns(2)
                with fig_col1:
                    st.markdown("###  maxLastMotorTorque")
                    fig2 = px.scatter(data_frame=data, x="x_column",y="maxLastMotorTorque")
                    st.write(fig2)
                with fig_col2:
                    st.markdown("### southSensorAngle")
                    fig1 = px.scatter(data_frame=data, x="x_column",y="southSensorAngle")
                    st.write(fig1)


                if st.session_state["df"] is not None:
                    st.download_button(
                        label="Download data as CSV",
                        data=convert_df(st.session_state["df"]),
                        file_name='large_df.csv',
                        mime='text/csv',
                    )



    except Exception as e:

        st.session_state["df"].to_csv('output.csv', index=False)
        print(e)


