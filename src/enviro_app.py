# Carbon Intensity & Rainfall App
import datetime, pandas as pd, streamlit as st
import matplotlib.pyplot as plt, matplotlib.dates as mdates, seaborn as sns

# Set-up
from pipeline_carbon import carbon_data
from utils import convert_df, rainfall_data, time_stats
sns.set()
st.set_page_config(layout="wide")

today = datetime.datetime.today()
today_str = datetime.datetime.strftime(today, '%d-%b-%Y')

### Sidebar ###
st.sidebar.header('App Controls 🎮')
st.sidebar.markdown('---')
st.sidebar.info(f'Current Date: {today_str}')

start = st.sidebar.date_input(label='Start Date', value = today)
end = st.sidebar.date_input(label='End Date', value = today)

# API data extract
@st.cache(allow_output_mutation=True)
def update_data():
    return carbon_data(start_date=start, end_date=end + datetime.timedelta(days=1)).run_pipeline()

df = update_data()
df.columns = df.columns.str.lower()

df['start'] = pd.to_datetime(df['start'])
df['end'] = pd.to_datetime(df['end'])
df['renewables %'] = df['biomass %'] + df['wind %'] + df['hydro %'] + df['solar %']
df['fossil fuels %'] = df['coal %'] + df['gas %']
df['unknown %'] = df['other %'] + df['imports %']
df['total %'] = df['renewables %'] + df['nuclear %'] + df['fossil fuels %'] + df['unknown %']

####################################
#### Carbon Intensity App Build ####
####################################

st.markdown('---')
st.header('Carbon Intensity ♻')
st.markdown('---')

st.markdown('**This API app shows forecasts for up to 2 days ahead plus historic data**')
st.markdown('If a long time period is selected the app may take some time to complete the API query.')

# Sidebar - Nation / DNO filter
names = df['name'].unique()
sel_box = st.sidebar.selectbox(label='Select Area', options=names)

# Apply data filters
df_time = df[df['name'] == sel_box].copy().reset_index(drop = True)

# Start & End for axis
started = df_time['start'].min().strftime('%d-%b')
ended = df_time['start'].max().strftime('%d-%b')

# Plot carbon intensity timeseries
fig_intensity = plt.figure(figsize=(10,6))

plt.plot(df_time['start'], df_time['intensity'])

# Change x-axis to HH:MM if looking at single day
if start == end:
    plt.title(f'{sel_box} Carbon Intensity \n{started}', size = 14)
    dtFmt = mdates.DateFormatter('%H:%M') 
else:
    plt.title(f'{sel_box} Carbon Intensity \n{started} to {ended}', size = 14)
    dtFmt = mdates.DateFormatter('%d-%b')

plt.ylabel('kg CO2 / kWh Equiv.')
plt.tight_layout()
plt.gca().xaxis.set_major_formatter(dtFmt) # apply the format to the desired axis
st.pyplot(fig_intensity)

# Plot energy mix time series
fig_energy = plt.figure(figsize=(10,6))

plt.plot(df_time['start'], df_time['fossil fuels %'])
plt.plot(df_time['start'], df_time['nuclear %'])
plt.plot(df_time['start'], df_time['renewables %'])

plt.ylabel('Generation %')
plt.ylim(0,100)
plt.legend(['Fossil Fuels', 'Nuclear', 'Renewables'])

if start == end:
    plt.title(f'{sel_box} Energy Mix \n{started}', size = 14)
    dtFmt = mdates.DateFormatter('%H:%M')
else:
    plt.title(f'{sel_box} Energy Mix \n{started} to {ended}', size = 14)
    dtFmt = mdates.DateFormatter('%d-%b')

plt.tight_layout()
plt.gca().xaxis.set_major_formatter(dtFmt) # apply the format to the desired axis
st.pyplot(fig_energy)

# Summary data table
df_chart = df[['name', 'intensity', 'renewables %', 'nuclear %', 'fossil fuels %', 'unknown %', 'total %']]
df_chart = df_chart.groupby(by = 'name').mean().sort_values(by='renewables %', ascending=False)

df_peak = df[['name', 'intensity', 'renewables %', 'nuclear %', 'fossil fuels %', 'unknown %', 'total %']]
df_peak = df_peak.groupby(by = 'name').max().sort_values(by='renewables %', ascending=False)

df_app = df_chart.copy()
df_app.iloc[:, 1:] = round(df_app.iloc[:, 1:], 1)

with st.expander('Show Data Tables'):
    st.markdown('Stats Table')
    st.dataframe(df_time.describe())

    st.markdown('---\n\nMean Table')
    st.dataframe(df_app)

    st.markdown('---\n\nMax Table')
    st.dataframe(df_peak)

    st.markdown('''
    In the above tables the data is in kg/kWh for intensity and the rest are percentages. \n
    ''')

### App Build ###
st.markdown('---')
st.header('''Rainfall Data 🌧''')
st.markdown('---')
df = rainfall_data()

# Map & time-series
st.map(df.rename(columns={'station_latitude': 'latitude', 'station_longitude': 'longitude'}))
st.line_chart(time_stats(df), height = 500)

# Data tables
groups = df.groupby(by = ['station_name'])

group_min = groups['value'].min()
group_avg = groups['value'].mean()
group_max = groups['value'].max()
group_len = groups['value'].count()

group_old = groups['timestamp'].min()
group_new = groups['timestamp'].max()

group_lat = groups['station_latitude'].max()
group_lon = groups['station_longitude'].max()

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

### Download buttons
st.sidebar.markdown('---')
st.sidebar.subheader('Download Datasets...')

st.sidebar.download_button(
    label="Download Rainfall Dataset", 
    data=convert_df(group_summary),
    file_name='rainfall_data.csv', 
    mime='text/csv')

st.sidebar.download_button(
    label="Download Carbon Intensity Dataset", 
    data=convert_df(df), 
    file_name='raw_ci_data.csv', 
    mime='text/csv') 