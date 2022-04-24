# ClimateApp 
import datetime as dt, pandas as pd, streamlit as st

from pipeline_carbon import carbon_data
from pipeline_rainfall import rainfall_data

# date config
year = dt.datetime.today().year
month = dt.datetime.today().month
day = dt.datetime.today().day

start = dt.date(year, month, day - 7)
end = dt.date(year, month, day)

# run pipelines
@st.cache
def run_pipelines():
    return carbon_data(start, end).run_pipeline(), rainfall_data()

app_data = run_pipelines()

carbon = app_data[0]
rain = app_data[1]

#######################################################
###################### App Build ######################
#######################################################

st.title('ClimateApp ♻')
st.markdown('---')

# Top row
col1, col2 = st.columns(2)

with col1:
    st.subheader('Carbon Intensity')


with col2:
    st.subheader('Rainfall')