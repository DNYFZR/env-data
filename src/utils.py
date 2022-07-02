import pandas as pd, streamlit as st

# Download converter
@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

# Source Data
@st.cache(allow_output_mutation=True)
def rainfall_data():
    url = 'https://raw.githubusercontent.com/iDataEngineer/Analytics-Engineering/main/data/RainfallData/SEPA_Monthly.csv'

    df = pd.read_csv(url, parse_dates=['timestamp'], index_col=0)
    df['Year'] = [i.year for i in df['timestamp']]

    for col in [ 'Unnamed: 0', 'station_no']:
        if col in df.columns:
            del df[col]

    return df

# Time series stats
@st.cache(allow_output_mutation=True)
def time_stats(base_data):
    dates = base_data['timestamp'].unique()
    time_data = pd.DataFrame(index=dates, columns=['Min Rainfall','Mean Rainfall', 'Max Rainfall'])

    for i in time_data.index:
        time_data.loc[i, 'Mean Rainfall'] = base_data[base_data['timestamp'] == i]['value'].mean().astype(int)
        time_data.loc[i, 'Max Rainfall'] = base_data[base_data['timestamp'] == i]['value'].max().astype(int)
        time_data.loc[i, 'Min Rainfall'] = base_data[base_data['timestamp'] == i]['value'].min().astype(int)
    
    return time_data