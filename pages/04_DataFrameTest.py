import streamlit as st
import pandas as pd
import glob
import plotly.express as px

st.set_page_config(page_title="DataFrame Demo", page_icon="📊")

st.markdown("# DataFrame Visualization")
st.sidebar.header("DataFrame Visualization")



@st.cache_data
def get_data(csv):
    df = pd.read_csv(csv)
    return df.set_index("times")


csv = st.selectbox(label="CSV_Data",options=glob.glob(r"csv_data\*.csv"))

if not csv:
    st.error("Please select at least one country.")
else:
    df = get_data(csv)
countries = st.multiselect(
    "Choose Parameters", options=list(df.keys())
)
if not countries:
    st.error("Please select at least one parameter.")
else:
    data = df[countries]
     
    
    fig = px.line(data_frame=data, y=countries)
    st.plotly_chart(fig)