''' SEPA Rainfall API ETL '''
import requests, pandas as pd, datetime as dt 

'''
Function: Extracts data from the SEPA rainfall API.

Returns: Tuple of station data table & API data table (column headers are station_no)

Saves: API data table & station data table (can be disabled buy setting save_table = False)
'''

# API ETL function
def sepa_api_extract(table_url, base_url, save_table = True):
    run_date = dt.datetime.today().strftime('%Y-%m-%d')
    
    # API test & station data 
    res = requests.get(table_url)
    if res.status_code != 200:
        print(f'Error ({res.status_code}), check API address')
    else:
        # Extract
        df_table = pd.DataFrame(res.json())
        df_table = df_table[['station_name', 'station_no', 'station_latitude', 'station_longitude']]
    
        # Transform
        df_table['station_no'] = df_table['station_no'].astype(int)
        df_table['station_latitude'] = df_table['station_latitude'].astype(float)
        df_table['station_longitude'] = df_table['station_longitude'].astype(float)

        # Identifiers for API extracts
        id_list = [i for i in df_table['station_no']]
        
        # Load to file
        if save_table == True:
            df_table.to_csv(f'SEPA_station_info ({run_date}).csv', index=None)

        # Data extract
        api = base_url.format(id_list[0])
        res = requests.get(api).json()
        df_data = pd.to_datetime(pd.DataFrame(res, columns = ['Timestamp'])) 

        for i in id_list:
            api = base_url.format(i)
            res = requests.get(api).json()
            add_col = pd.DataFrame(res, columns = ['Value'])
            add_col['Value'] = add_col['Value'].astype(float)
            add_col['Value'] = [0.0 if pd.isna(i) else i for i in add_col['Value']]
            add_col = add_col.rename(columns = {'Value': i})

            df_data = pd.concat([df_data, add_col[i]], axis = 1)
        
        # Load to file
        df_data.to_csv(f'SEPA_rainfall_data ({run_date}).csv', index=None)
        
        return (df_table, df_data)

# Test
if __name__ == "__main__":
    # Station data 
    table_url = 'https://apps.sepa.org.uk/rainfall/api/Stations'
    
    # Daily data
#     daily_url = 'https://apps.sepa.org.uk/rainfall/api/Daily/{}?all=true'
#     df_daily = sepa_api_extract(table_url, daily_url)

    # Monthly data
    monthly_url = 'https://apps.sepa.org.uk/rainfall/api/Month/{}?all=true'
    df_monthly = sepa_api_extract(table_url, monthly_url)
