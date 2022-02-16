'''Rainfall Map App'''
import pandas as pd, streamlit as st
### Functions ###

# Download converter
@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

# Source Data
@st.cache(allow_output_mutation=True)
def source_data():
    url = 'https://raw.githubusercontent.com/sciDelta/API-ETL-SEPA-rainfall/main/data/SEPA_Monthly.csv'

    df = pd.read_csv(url, parse_dates=['Timestamp'])
    df['Year'] = [i.year for i in df['Timestamp']]

    for col in [ 'Unnamed: 0', 'station_no', 'station_number']:
        if col in df.columns:
            del df[col]

    return df

df = source_data()

# Time series stats
@st.cache(allow_output_mutation=True)
def time_stats(base_data):
    dates = base_data['Timestamp'].unique()
    time_data = pd.DataFrame(index=dates, columns=['Min Rainfall','Mean Rainfall', 'Max Rainfall'])

    for i in time_data.index:
        time_data.loc[i, 'Mean Rainfall'] = base_data[base_data['Timestamp'] == i]['Rainfall (mm)'].mean().astype(int)
        time_data.loc[i, 'Max Rainfall'] = base_data[base_data['Timestamp'] == i]['Rainfall (mm)'].max().astype(int)
        time_data.loc[i, 'Min Rainfall'] = base_data[base_data['Timestamp'] == i]['Rainfall (mm)'].min().astype(int)
    
    return time_data

### App Build ###
st.title('''🌧 Scottish Rainfall Data App 🌧''')

# Location filter (sidebar)
filter_station = [i for i in df['station_name'].sort_values(ascending=True).unique()]
st.sidebar.subheader('Select Location')
selected_station = st.sidebar.multiselect(label = '', options= filter_station)

# Year filter (sidebar)
filter_year = [i for i in df['Year'].sort_values(ascending=False).unique()]
st.sidebar.subheader('Select Year')
selected_year = st.sidebar.multiselect(label = '', options= filter_year)

# Map data filters
if selected_station == [] and selected_year == []:
    map_data = df.copy()
elif selected_station == [] and selected_year != 'All':
    map_data = df[df['Year'].isin(selected_year)].copy()
elif selected_station != [] and selected_year == []:
    map_data = df[df['station_name'].isin(selected_station)].copy()
else:
    map_data = df[(df['Year'].isin(selected_year)) & (df['station_name'].isin(selected_station))].copy()

map_chart = map_data.copy().drop(columns=['Year']).reset_index(drop = True)

# Map & time series chart
map_col, chart_col = st.columns(2)
with map_col: 
    st.map(map_chart)
with chart_col:
    st.line_chart(time_stats(map_chart), height = 500)

# Data tables
groups = map_chart.groupby(by = ['station_name'])

group_min = groups['Rainfall (mm)'].min()
group_avg = groups['Rainfall (mm)'].mean()
group_max = groups['Rainfall (mm)'].max()
group_len = groups['Rainfall (mm)'].count()

group_old = groups['Timestamp'].min()
group_new = groups['Timestamp'].max()

group_lat = groups['latitude'].max()
group_lon = groups['longitude'].max()

group_summary = pd.concat([
    group_min.rename('Min (mm)'), 
    group_avg.rename('Mean (mm)'), 
    group_max.rename('Max (mm)'),
    group_len.rename('Count'),
    group_lat.rename('Latitude'),
    group_lon.rename('Longitude'),
    group_old.rename('Oldest'),
    group_new.rename('Most recent')
    ], axis=1)

with st.expander('Show data table'):
    st.subheader('Site by Site Summary')
    st.dataframe(group_summary)

# Download options (sidebar)
st.sidebar.subheader('Download Summary Data')
st.sidebar.download_button(
    label="Download Data", 
    data=convert_df(group_summary),
    file_name='summary_data.csv', 
    mime='text/csv')

st.sidebar.subheader('Download Base Data')
st.sidebar.download_button(
    label="Download Data", 
    data=convert_df(map_chart),
    file_name='base_data.csv', 
    mime='text/csv')
