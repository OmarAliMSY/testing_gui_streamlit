import pandas as pd
import streamlit as st
import pandas_profiling
import glob
from streamlit_pandas_profiling import st_profile_report



csv = st.selectbox(label="CSV_Data",options=glob.glob(r"csv_data/*.csv", recursive=True))

if csv:
    df = pd.read_csv(csv)
    pr = df.profile_report()

    st_profile_report(pr)