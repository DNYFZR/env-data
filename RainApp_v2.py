'''Rainfall Map App'''
import pandas as pd, streamlit as st
### Functions ###

# Source Data
@st.cache(allow_output_mutation=True)
def source_data():
    url = 'https://raw.githubusercontent.com/sciDelta/API-ETL-SEPA-rainfall/main/data/SEPA_Monthly.csv'

    df = pd.read_csv(url, parse_dates=['Timestamp'])
    df = df.drop(columns = ['Station_no', 'Station_number'])
    df['Year'] = [i.year for i in df['Timestamp']]
    df['Rainfall'] = df['Rainfall'].astype(int)

    return df

df = source_data()

# Download converter
@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

# Time series stats
@st.cache(allow_output_mutation=True)
def time_stats(base_data):
    dates = base_data['Timestamp'].unique()
    time_data = pd.DataFrame(index=dates, columns=['Min Rainfall','Mean Rainfall', 'Max Rainfall'])

    for i in time_data.index:
        time_data.loc[i, 'Mean Rainfall'] = base_data[base_data['Timestamp'] == i]['Rainfall'].mean().astype(int)
        time_data.loc[i, 'Max Rainfall'] = base_data[base_data['Timestamp'] == i]['Rainfall'].max().astype(int)
        time_data.loc[i, 'Min Rainfall'] = base_data[base_data['Timestamp'] == i]['Rainfall'].min().astype(int)
    
    return time_data

### App Build ###
st.title('''Scottish Rainfall API Data''')

# Filters
col1, col2 = st.columns(2)

filter_station = ['All']
for i in df['Station Name'].sort_values(ascending=True).unique():
    filter_station.append(i)
selected_station = col1.selectbox('Station', filter_station)

filter_year = ['All']
for i in df['Year'].sort_values(ascending=False).unique():
    filter_year.append(i)
selected_year = col2.selectbox('Year', filter_year)

# Map data
if selected_station == 'All' and selected_year == 'All':
    map_data = df.copy()
elif selected_station == 'All' and selected_year != 'All':
    map_data = df[df['Year'] == int(selected_year)].copy()
elif selected_station != 'All' and selected_year == 'All':
    map_data = df[df['Station Name'] == selected_station].copy()
else:
    map_data = df[(df['Year'] == int(selected_year)) & (df['Station Name'] == selected_station)].copy()

map_chart = map_data.copy().drop(columns=['Year'])

# Map viz
st.map(map_chart)
map_chart

st.download_button(
    label="Download Mapped Data", 
    data=convert_df(map_chart),
    file_name='map_data.csv', 
    mime='text/csv')

# Time series chart & table
st.header('Rainfall Over Time')
time_data = time_stats(map_chart)

time_chart = time_data.copy()
time_chart.index = time_chart.index.map({k: pd.to_datetime(k, format='%d-%m-%Y') for k in time_chart.index})
st.line_chart(time_chart)

time_data 

# Download option
st.download_button(
    label="Download Summary Data", 
    data=convert_df(time_data), 
    file_name='all_data.csv', 
    mime='text/csv')
