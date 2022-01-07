#### Streamlit App - Carbon Intensity Dashboard ###
import datetime, pandas as pd, streamlit as st
import matplotlib.pyplot as plt, matplotlib.dates as mdates, seaborn as sns
from pandas.core.indexes.datetimes import date_range
from DataPipeline import get_api_data
sns.set()

st.title('Carbon Intensity App')
today = datetime.datetime.today()

# Download data converter
@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

# Select dates
col1, col2 = st.columns(2)

start = col1.date_input(label='Start Date', value = datetime.date(2022, 1, 1))
start_str = datetime.datetime.strftime(start, '%Y-%m-%d')

end = col2.date_input(label='End Date')
end_str = datetime.datetime.strftime(end, '%Y-%m-%d')

# API data extract
@st.cache
def update_data():
    return get_api_data(start_date=start, end_date=end)

df = update_data()

# Carbon Intensity tracker
names = df['shortname'].unique()
sel_box = st.selectbox(label='Select Area', options=names, index = 17)

df_cop = df[df['shortname'] == sel_box][['start date', 'intensity']].copy().reset_index(drop = True)
df_cop['start date'] = pd.to_datetime(df_cop['start date'])

fig_intensity = plt.figure(figsize=(10,6))

plt.plot(df_cop['start date'], df_cop['intensity'], )

started = df_cop['start date'].min().strftime('%d-%b')
ended = df_cop['start date'].max().strftime('%d-%b')

plt.title(f'{sel_box} Carbon Intensity \n{started} to {ended}', size = 14)
plt.tight_layout()

dtFmt = mdates.DateFormatter('%b-%d') # define the formatting
plt.gca().xaxis.set_major_formatter(dtFmt) # apply the format to the desired axis

st.pyplot(fig_intensity)

# Time series
df_t = df[df['shortname'] == sel_box].copy()

df_t['Renewables'] = df_t['biomass'] + df_t['wind'] + df_t['hydro'] + df_t['solar']
df_t['Fossil Fuels'] = df_t['coal'] + df_t['gas']
df_t['start date'] = pd.to_datetime(df_t['start date'])
df_t = df_t.rename(columns = {'nuclear': 'Nuclear'})

fig_time = plt.figure(figsize=(10,6))

plt.plot(df_t['start date'], df_t['Fossil Fuels'], )
plt.plot(df_t['start date'], df_t['Nuclear'], )
plt.plot(df_t['start date'], df_t['Renewables'], )

started = df_t['start date'].min().strftime('%d-%b')
ended = df_t['start date'].max().strftime('%d-%b')

plt.title(f'{sel_box} Energy Sources \n{started} to {ended}', size = 14)
plt.ylabel('Supply %')
plt.ylim(0,100)
plt.legend(['Gas', 'Nuclear', 'Renewables'])
plt.tight_layout()

dtFmt = mdates.DateFormatter('%b-%d') # define the formatting
plt.gca().xaxis.set_major_formatter(dtFmt) # apply the format to the desired axis

st.pyplot(fig_time)
st.download_button(
    label="Download Data", 
    data=convert_df(df_t), 
    file_name='data.csv', 
    mime='text/csv',
    )


# Summary data
@st.cache(allow_output_mutation=True)
def chart_data(df_mix):
    # Average for each DNO
    dno_list = [i for i in df_mix['shortname'].unique()]
    cols = ['intensity', 'biomass', 'coal', 'imports', 'gas', 'nuclear', 'other', 'hydro', 'solar', 'wind']
    df_dno_avg = pd.DataFrame(index = range(len(dno_list)), data = dno_list, columns=['DNO Name'])

    for c in cols:
        new_col = {}
        temp_df = df_mix[['shortname', c]]
        for n, i in enumerate(dno_list):
            temp_val = temp_df[temp_df['shortname'] == i][c].mean()
            new_col.update({n: temp_val})
        df_dno_avg[c] = df_dno_avg.index.map(new_col)

    total_col = {}
    for i in df_dno_avg.index:
        temp_val = df_dno_avg.iloc[i, :]
        temp_val = sum(temp_val[-len(cols):]) - df_dno_avg.loc[i, 'intensity']
        total_col.update({i: temp_val})

    df_dno_avg['total'] = df_dno_avg.index.map(total_col)

    return df_dno_avg

df_chart = chart_data(df)


# Pie charts
dno_list = [i for i in df['shortname'].unique()]

# Chart 1
df_chart['fossil'] = df_chart['coal'] + df_chart['gas'] 
df_chart['renewable'] = df_chart['wind'] + df_chart['solar'] + df_chart['biomass'] + df_chart['hydro']
df_chart['unknown'] = df_chart['other'] + df_chart['imports']

df_plot = df_chart[['DNO Name', 'fossil', 'nuclear', 'renewable', 'unknown']].set_index('DNO Name')

id_list = dno_list.copy()
n_rows = 6
n_cols = 3

fig, ax = plt.subplots(nrows = n_rows, ncols = n_cols, figsize = (20, 30))
for row in range(n_rows):
    for col in range(n_cols):
        i = id_list[0]

        ax[row, col].pie(
            x = df_plot.loc[i, ['fossil', 'nuclear', 'renewable', 'unknown']],
            autopct = '%.0f%%', textprops={'fontsize': 14, 'color': 'black'}, pctdistance = 1.15)
        if i == 'GB':
            ax[row, col].set_title(i, fontsize = 16)
        else:
            ax[row, col].set_title(i.title(), fontsize = 16)

        # Remove used ID & column from list
        id_list.pop(0)

fig.legend(['Fossil', 'Nuclear', 'Renewable', 'Imports'], 
            loc = 'lower center', facecolor = 'gainsboro', 
            prop={'size': 14}, ncol = 4, frameon = False,
            bbox_to_anchor=(0.5, 0.075))

plt.rcParams['figure.facecolor'] = 'gainsboro'
plt.suptitle('Generation Mix By Area', y = 0.93, fontsize = 18, fontweight = 'semibold')

st.pyplot(fig = fig)
st.dataframe(df_plot.round(1))

