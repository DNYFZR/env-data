#### Streamlit App - Carbon Intensity Dashboard ###
import datetime, pandas as pd, streamlit as st
import matplotlib.pyplot as plt, matplotlib.dates as mdates, seaborn as sns
from DataPipeline import carbon_data
sns.set()

### Set Up ###

# Wide Mode 
def auto_wide_mode():
    st.set_page_config(layout="wide")

auto_wide_mode()

# Download data converter
@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

today = datetime.datetime.today()
today_str = datetime.datetime.strftime(today, '%d-%b-%Y')

# Sidebar Dates
st.sidebar.subheader('🎮 App Controls 🎮')
st.sidebar.text(f'Current Date: {today_str}')

start = st.sidebar.date_input(label='Start Date', value = today)
end = st.sidebar.date_input(label='End Date', value = today)

data_pipeline = carbon_data(start_date=start, end_date=end + datetime.timedelta(days=1))

# API data extract
@st.cache(allow_output_mutation=True)
def update_data():
    return data_pipeline.run_pipeline()

df = update_data()

df.columns = df.columns.str.lower()

df['start'] = pd.to_datetime(df['start'])
df['end'] = pd.to_datetime(df['end'])
df['renewables %'] = df['biomass %'] + df['wind %'] + df['hydro %'] + df['solar %']
df['fossil fuels %'] = df['coal %'] + df['gas %']
df['unknown %'] = df['other %'] + df['imports %']
df['total %'] = df['renewables %'] + df['nuclear %'] + df['fossil fuels %'] + df['unknown %']


### App Build ###
st.title('♻ Carbon Intensity App ♻')

st.markdown('**This app can show forecasts for up to 2 days ahead as well as historic data**')
st.markdown('If a long time period is selected the app may take some time to complete the API query.')

# Sidebar - Nation / DNO filter
names = df['name'].unique()
sel_box = st.sidebar.selectbox(label='Select Area', options=names, index = 17)

### Filter & Plot Timeseries ###

# set up cols for intensity & energy mix charts
col1, col2 = st.columns(2)

# Apply data filters
df_time = df[df['name'] == sel_box].copy().reset_index(drop = True)

# Start & End for axis
started = df_time['start'].min().strftime('%d-%b')
ended = df_time['start'].max().strftime('%d-%b')

# Plot carbon intensity timeseries
fig_intensity = plt.figure(figsize=(10,10))

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

# plot in first column
with col1:
    st.pyplot(fig_intensity)

# Plot energy mix time series
fig_energy = plt.figure(figsize=(10,10))

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

with col2:
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

# Energy mix pies
df_pies = df_app.copy()

id_list = [i for i in df['name'].copy().unique()]
n_rows = 6
n_cols = 3

pie_fig, ax = plt.subplots(nrows = n_rows, ncols = n_cols, figsize = (12, 14))
for row in range(n_rows):
    for col in range(n_cols):
        i = id_list[0]

        ax[row, col].pie(
            x = df_pies.loc[i, ['fossil fuels %', 'nuclear %', 'renewables %', 'unknown %']],
            autopct = '%.0f%%', textprops={'fontsize': 8, 'color': 'black'}, pctdistance = 1.225)
        if i == 'GB':
            ax[row, col].set_title(i, fontsize = 10)
        else:
            ax[row, col].set_title(i.title(), fontsize = 10)

        # Remove used ID & column from list
        id_list.pop(0)

pie_fig.legend(['Fossil', 'Nuclear', 'Renewable', 'Imports'], 
            loc = 'lower center', facecolor = 'gainsboro', 
            prop={'size': 10}, ncol = 4, frameon = False,
            bbox_to_anchor=(0.5, 0.075))

plt.rcParams['figure.facecolor'] = 'gainsboro'
plt.suptitle('Generation Mix By Area', y = 0.93, fontsize = 12, fontweight = 'semibold')

st.pyplot(pie_fig)

### Download buttons
st.sidebar.subheader('Download Datasets...')

st.sidebar.download_button(
    label="Download Time Series (raw)", 
    data=convert_df(df_time), 
    file_name='time_data.csv', 
    mime='text/csv') 

st.sidebar.download_button(
    label="Download Time Series (mean)", 
    data=convert_df(df_chart), 
    file_name='chart_data.csv', 
    mime='text/csv') 

st.sidebar.download_button(
    label="Download Time Series (max)", 
    data=convert_df(df_peak), 
    file_name='chart_data.csv', 
    mime='text/csv') 

st.sidebar.download_button(
    label="Download Raw Dataset", 
    data=convert_df(df), 
    file_name='raw_data.csv', 
    mime='text/csv') 