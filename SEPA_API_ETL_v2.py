''' SEPA Rainfall API ETL '''
import requests, pandas as pd, datetime as dt

# API ETL function
def sepa_api_extract(table_url, base_url):    
    # API check
    api_status = requests.get(table_url).status_code
    
    if api_status != 200:
        return pd.Series(data = api_status, name='Current API Status')

    else:
        # Station data 
        res = requests.get(table_url)
        df_table = pd.DataFrame(res.json())
        df_table = df_table[['station_name', 'station_no', 'station_latitude', 'station_longitude']]

        # Transform
        df_table['station_no'] = df_table['station_no'].astype(int)
        df_table['station_latitude'] = df_table['station_latitude'].astype(float)
        df_table['station_longitude'] = df_table['station_longitude'].astype(float)

        # Identifiers for API extracts
        id_list = [i for i in df_table['station_no']]

        # Data extract
        df_data = pd.DataFrame()
        for i in id_list:
            api = base_url.format(i)
            res = requests.get(api).json()
            add_col = pd.DataFrame(res, columns = ['Timestamp', 'Value'])
            add_col['station_number'] = i
            df_data = pd.concat([df_data, add_col], axis = 0)

        df_data['Value'] = df_data['Value'].astype(float)
        df_data['Value'] = [0.0 if pd.isna(i) or i == '' else i for i in df_data['Value']]
        df_data = df_data.rename(columns = {'Value': 'Rainfall (mm)'})
        df_data['Timestamp'] = pd.to_datetime(df_data['Timestamp'])

        # Combine data 
        station_name = {}
        station_no = {}
        latitude = {}
        longitude = {}
        for i in df_data['station_number'].unique():
            if i not in station_name.keys():
                station_name.update({i: df_table[df_table['station_no'] == i].reset_index().loc[0, 'station_name']})
            if i not in station_no.keys():
                station_no.update({i: df_table[df_table['station_no'] == i].reset_index().loc[0, 'station_no']})
            if i not in latitude.keys():
                latitude.update({i: df_table[df_table['station_no'] == i].reset_index().loc[0, 'station_latitude']})
            if i not in longitude.keys():
                longitude.update({i: df_table[df_table['station_no'] == i].reset_index().loc[0, 'station_longitude']})
        
        df_data['station_name'] = df_data['station_number'].map(station_name)
        df_data['station_no'] = df_data['station_number'].map(station_no)
        df_data['latitude'] = df_data['station_number'].map(latitude)
        df_data['longitude'] = df_data['station_number'].map(longitude)
        
        return df_data

if __name__ == '__main__':
    # run API call on monthly data
    today = dt.datetime.strftime(dt.datetime.today(), '%Y-%b-%d')
    
    table_url = 'https://apps.sepa.org.uk/rainfall/api/Stations'
    monthly_url = 'https://apps.sepa.org.uk/rainfall/api/Month/{}?all=true'
    
    rainfall_data = sepa_api_extract(table_url, monthly_url)

    rainfall_data.to_csv(r'data/SEPA_Monthly_{}.csv'.format(today))