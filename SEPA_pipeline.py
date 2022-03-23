''' SEPA Rainfall API ETL '''

import requests, pandas as pd

###################################################################################

def station_data(table_url):
    ''' Function takes in the SEPA rainfall API station table URL and checks if the API is returning a 200 status code. 
        
        If not, the function prints error statement with current status code. 
        
        Else, creates a dataframe with the metadata, and returns the table with the station name, number, latitude & longitude.

        The table is utilised by the monthly_data() function to extract data from the API and then tag it to the correct site.   
    '''
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

##############################################################################################

def monthly_data(monthly_url, table_url):
    ''' Function takes in the URLs for the API data feed (monthly_url) & the metadata (table_url). 
        
        It calls the station_data() function, then creates dictionaries of the station name, latitude & longitude, with the key set to the station number. 
    '''

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
        url = monthly_url.format(idx)
        api_call = requests.get(url).json()

        # Add station no (id) to dict & append to combined dataset
        for data_dict in api_call:
            data_dict['station_no'] = idx
            combined_data.append(data_dict)

    # map additional data to dictionaries from ref's
    for data_dict in combined_data:
        data_dict['station_name'] = station_names[data_dict['station_no']]
        data_dict['station_latitude'] = station_lat[data_dict['station_no']]
        data_dict['station_longitude'] = station_lon[data_dict['station_no']]

    # create output data frame
    combined_data = pd.DataFrame(combined_data)
    combined_data.columns = [i.lower() for i in combined_data.columns]
    combined_data['timestamp'] = pd.to_datetime(combined_data['timestamp'])
    return combined_data


if __name__ == '__main__':
    # Extract API data
    table_url = 'https://www2.sepa.org.uk/rainfall/api/Stations'
    monthly_url = 'https://www2.sepa.org.uk/rainfall/api/Month/{}?all=true'

    data = monthly_data(table_url=table_url, monthly_url=monthly_url)

    # Check most recent timestamp in database
    database = pd.read_csv(r'data/SEPA_Monthly.csv', index_col=0, parse_dates=['timestamp'])
    last_entry_date = database['timestamp'].max()

    # Copy new data to database - filter for entries more recent than last db update.
    database_updated = pd.concat([database, data[data['timestamp'] > last_entry_date]], axis = 0)
    database_updated.to_csv(r'data/SEPA_Monthly.csv')