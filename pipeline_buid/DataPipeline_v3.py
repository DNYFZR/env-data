### Carbon Intensity API Data Pipeline ###
import requests, pandas as pd, datetime as dt
from time import time
run_start = time()


def extract_data( start_date = dt.date(2022,1,1), end_date = dt.date(2022,4,1) ):
    '''
    Function calls the API url and returns the JSON data structure between teh selected dates
    '''

    api_url ='https://api.carbonintensity.org.uk/regional/intensity/{}T00:30Z/{}T00:00Z'
    api_headers = {'Accept': 'application/json'}
    
    date_list = list()

    # Create list of dates for URL
    if start_date == end_date:
        date_list.append( (str(start_date), str(end_date + dt.timedelta(days = 1)) ) )
    else:
        i = start_date
        while i < end_date:
            first = i        
            last = i + dt.timedelta(days = 1) 
            date_list.append( (str(first), str(last)) )
            i += dt.timedelta(days = 1)

    # Extract JSON from API and append to list
    api_json = list()
    for i in range(len(date_list)):
        url = api_url.format(date_list[i][0], date_list[i][1])
        req = requests.get(url, params={}, headers = api_headers).json()
        api_json.append(req)

    return api_json

def load_data(dataset = extract_data()):
    # Set up columns
    start_dates, end_dates = list(), list()
    data_nest = list()

    # Extract dates from 1st level JSON
    for json_nest in dataset:
        json_nest = json_nest['data']

        [start_dates.append(i['from']) for i in json_nest]
        [end_dates.append(i['to']) for i in json_nest]
        [data_nest.append(i['regions']) for i in json_nest]

    # Create & update output table
    output_table = pd.DataFrame()

    output_table['Start'] = [pd.to_datetime(i) for i in start_dates]
    output_table['End'] = [pd.to_datetime(i) for i in end_dates]
    output_table['data']  = data_nest
    
    return output_table

def transform_data():
    # Set up containers
    table = load_data()
    output = pd.DataFrame()
    
    start, end, ids, names, intensity, energy = list(), list(), list(), list(), list(), list()

    # Transform data structure
    for row, data in enumerate(table['data'].copy()):
        start_date = table.loc[row, 'Start']
        end_date = table.loc[row, 'End']

        for region in data:
            start.append(start_date)
            end.append(end_date)
            ids.append(region['regionid'])
            names.append(region['shortname'])
            intensity.append(region['intensity']) 
            energy.append(region['generationmix']) 

    output['Start'] = start
    output['End'] = end
    output['ID'] = ids
    output['Name'] = names
    output['Intensity'] = [i['forecast'] for i in intensity]
    output['Intensity Category'] = [i['index'] for i in intensity]
    output['Energy Mix'] = energy
    
    return output

def transform_energy():
    table = transform_data()
    
    # Set up containers for energy mix extraction
    biomass,hydro, solar, wind = list(), list(), list(), list()
    coal, gas = list(), list()
    nuclear = list()
    imports, other = list(), list()

    energy = table['Energy Mix'].copy()
    for mix in energy:
        for idx in range(len(mix)):
            if mix[idx]['fuel'] == 'biomass':
                biomass.append(mix[idx]['perc'])
            if mix[idx]['fuel'] == 'hydro':
                hydro.append(mix[idx]['perc'])
            if mix[idx]['fuel'] == 'solar':
                solar.append(mix[idx]['perc'])
            if mix[idx]['fuel'] == 'wind':
                wind.append(mix[idx]['perc'])
            
            if mix[idx]['fuel'] == 'coal':
                coal.append(mix[idx]['perc'])
            if mix[idx]['fuel'] == 'gas':
                gas.append(mix[idx]['perc'])
            
            if mix[idx]['fuel'] == 'nuclear':
                nuclear.append(mix[idx]['perc'])
            
            if mix[idx]['fuel'] == 'imports':
                imports.append(mix[idx]['perc'])
            if mix[idx]['fuel'] == 'other':
                other.append(mix[idx]['perc'])

    table['Biomass %'] = biomass
    table['Hydro %'] = hydro
    table['Solar %'] = solar
    table['Wind %'] = wind
    table['Coal %'] = coal
    table['Gas %'] = gas
    table['Nuclear %'] = nuclear
    table['Imports %'] = imports
    table['Other %'] = other
    
    del table['Energy Mix']
    return table

if __name__ == '__main__':
    test = transform_energy()

    print(f'Run time: {round(time() - run_start, 1)}s')