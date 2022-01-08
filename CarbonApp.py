#### Streamlit App - Carbon Intensity Dashboard ###
import datetime, pandas as pd, streamlit as st
import matplotlib.pyplot as plt, matplotlib.dates as mdates, seaborn as sns
from DataPipeline import get_api_data
sns.set()

st.title('♻ Carbon Intensity App ♻')
st.markdown('**This app can show forecasts for up to 2 days ahead as well as historic data**')
st.markdown('Developer: Daniel [@sciDelta](https://twitter.com/sciDelta)')
today = datetime.datetime.today()

# Download data converter
@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

# Select dates
col1, col2 = st.columns(2)

start = col1.date_input(label='Start Date', value = today)
end = col2.date_input(label='End Date', value = today)

# API data extract
@st.cache(allow_output_mutation=True)
def update_data():
    return get_api_data(start_date=start, end_date=end + datetime.timedelta(days=1))

df = update_data()

df['start date'] = pd.to_datetime(df['start date'])
df['end date'] = pd.to_datetime(df['end date'])
df['renewables'] = df['biomass'] + df['wind'] + df['hydro'] + df['solar']
df['fossil fuels'] = df['coal'] + df['gas']
df['unknown'] = df['other'] + df['imports']

# Time Series Charts / Table
names = df['shortname'].unique()
sel_box = st.selectbox(label='Select Area', options=names, index = 17)

df_time = df[df['shortname'] == sel_box].copy().reset_index(drop = True)

# Plot charts
started = df_time['start date'].min().strftime('%d-%b')
ended = df_time['end date'].max().strftime('%d-%b')

fig_intensity = plt.figure(figsize=(10,6))

plt.plot(df_time['start date'], df_time['intensity'])

if start == end:
    plt.title(f'{sel_box} Carbon Intensity \n{started}', size = 14)
    dtFmt = mdates.DateFormatter('%H:%M') 
else:
    plt.title(f'{sel_box} Carbon Intensity \n{started} to {ended}', size = 14)
    dtFmt = mdates.DateFormatter('%d-%b')

plt.tight_layout()
plt.gca().xaxis.set_major_formatter(dtFmt) # apply the format to the desired axis

st.pyplot(fig_intensity)

fig_energy = plt.figure(figsize=(10,6))

plt.plot(df_time['start date'], df_time['fossil fuels'])
plt.plot(df_time['start date'], df_time['nuclear'])
plt.plot(df_time['start date'], df_time['renewables'])

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

st.download_button(
    label="Download Chart Data", 
    data=convert_df(df_time), 
    file_name='time_data.csv', 
    mime='text/csv') 


# Summary data
st.subheader('Average For Selected Time Period')
@st.cache(allow_output_mutation=True)
def chart_data(dataframe):
    # Average for each DNO
    dno_list = [i for i in dataframe['shortname'].unique()]
    cols = ['intensity', 'biomass', 'coal', 'imports', 'gas', 'nuclear', 'other', 'hydro', 'solar', 'wind']
    df_out = pd.DataFrame(index = range(len(dno_list)), data = dno_list, columns=['DNO Name'])

    for c in cols:
        new_col = {}
        temp_df = dataframe[['shortname', c]]
        for n, i in enumerate(dno_list):
            temp_val = temp_df[temp_df['shortname'] == i][c].mean()
            new_col.update({n: temp_val})
        df_out[c] = df_out.index.map(new_col)

    total_col = {}
    for i in df_out.index:
        temp_val = df_out.iloc[i, :]
        temp_val = sum(temp_val[-len(cols):]) - df_out.loc[i, 'intensity']
        total_col.update({i: temp_val})

    df_out['total'] = df_out.index.map(total_col)

    df_out['renewables'] = df_out['biomass'] + df_out['wind'] + df_out['hydro'] + df_out['solar']
    df_out['fossil fuels'] = df_out['coal'] + df_out['gas']
    df_out['unknown'] = df_out['other'] + df_out['imports']

    return df_out

df_chart = chart_data(df.copy())
df_chart

st.download_button(
    label="Download Summary Data", 
    data=convert_df(df_chart), 
    file_name='chart_data.csv', 
    mime='text/csv') 

# Pies 
df_pies = df_chart[['DNO Name', 'fossil fuels', 'nuclear', 'renewables', 'unknown']].copy().set_index('DNO Name', drop=True)


id_list = [i for i in df['shortname'].copy().unique()]
n_rows = 6
n_cols = 3

pie_fig, ax = plt.subplots(nrows = n_rows, ncols = n_cols, figsize = (20, 30))
for row in range(n_rows):
    for col in range(n_cols):
        i = id_list[0]

        ax[row, col].pie(
            x = df_pies.loc[i, ['fossil fuels', 'nuclear', 'renewables', 'unknown']],
            autopct = '%.0f%%', textprops={'fontsize': 14, 'color': 'black'}, pctdistance = 1.15)
        if i == 'GB':
            ax[row, col].set_title(i, fontsize = 16)
        else:
            ax[row, col].set_title(i.title(), fontsize = 16)

        # Remove used ID & column from list
        id_list.pop(0)

pie_fig.legend(['Fossil', 'Nuclear', 'Renewable', 'Imports'], 
            loc = 'lower center', facecolor = 'gainsboro', 
            prop={'size': 14}, ncol = 4, frameon = False,
            bbox_to_anchor=(0.5, 0.075))

plt.rcParams['figure.facecolor'] = 'gainsboro'
plt.suptitle('Generation Mix By Area', y = 0.93, fontsize = 18, fontweight = 'semibold')

st.pyplot(pie_fig)

st.download_button(
    label="Download Raw Data", 
    data=convert_df(df), 
    file_name='raw_data.csv', 
    mime='text/csv') 