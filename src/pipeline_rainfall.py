''' Rainfall API ETL '''
import requests, pandas as pd

# API ETL function
def station_data(table_url):
    api_test = requests.get(table_url).status_code
    if api_test != 200:
        print(f'API error {api_test}')
    else:
        station_data = pd.DataFrame(requests.get(table_url).json())
        
        for col in station_data.columns:
            if col not in ['station_name', 'station_latitude', 'station_longitude', 'station_no']:
                del station_data[col]
        
        station_data['station_latitude'] = station_data['station_latitude'].astype(float)
        station_data['station_longitude'] = station_data['station_longitude'].astype(float)
        station_data['station_no'] = station_data['station_no'].astype(int)
        return station_data

def data_etl(hourly_url, table_url):
    # Create reference dictionaries
    temp_df = station_data(table_url).set_index('station_no', drop = True)
    station_names = temp_df['station_name'].to_dict()
    station_lat = temp_df['station_latitude'].to_dict()
    station_lon = temp_df['station_longitude'].to_dict()

    # ID stack
    id_stack = [i for i in temp_df.index]
    
    # API call
    combined_data = []
    for idx in id_stack:
        url = hourly_url.format(idx)
        api_call = requests.get(url).json()

        # Add station no to dict then append to combined data list
        for data_dict in api_call:
            data_dict['station_no'] = idx
            combined_data.append(data_dict)

    # map additional data to dictionaries
    for data_dict in combined_data:
        data_dict['station_name'] = station_names[data_dict['station_no']]
        data_dict['station_latitude'] = station_lat[data_dict['station_no']]
        data_dict['station_longitude'] = station_lon[data_dict['station_no']]

    # create data frame
    combined_data = pd.DataFrame(combined_data)
    combined_data.columns = [i.lower() for i in combined_data.columns]
    combined_data['timestamp'] = pd.to_datetime(combined_data['timestamp'])
    return combined_data


if __name__ == '__main__':
    from time import time
    print(f'Run initiated')
    # Extract API data
    table_url = 'https://www2.sepa.org.uk/rainfall/api/Stations'
    hourly_url = 'https://www2.sepa.org.uk/rainfall/api/Hourly/{}?today'

    start = time()    
    data = data_etl(table_url=table_url, hourly_url=hourly_url)
    print(data.head(), f'\nComplete in: {round(time() - start, 1)}s')