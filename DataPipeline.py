#### Carbon Intensity API Pipeline ####
import requests, pandas as pd, datetime as dt

# Wrapper function for API extract
def get_api_data(start_date, end_date):
    if type(start_date) == str:
        start_date = pd.to_datetime(start_date)
    if type(end_date) == str:
        end_date = pd.to_datetime(end_date)

    api_url = 'https://api.carbonintensity.org.uk/regional/intensity/{}T00:30Z/{}T00:00Z'
    headers = {'Accept': 'application/json'}

    df_mix = pd.DataFrame()
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

    # Extract JSON from API
    for i in range(len(date_list)):
        url = api_url.format(date_list[i][0], date_list[i][1])
        req = requests.get(url, params={}, headers = headers)

        for j in range(48): # 48 half hours per day
            if len(req.json()['data']) <= j: 
                pass
            else:
                df = pd.DataFrame(req.json()['data'][j]['regions'])
                df['intensity'] = [i['forecast'] for i in df['intensity']]

                # Start & end timestamps
                df['start date'] = req.json()['data'][j]['from']
                df['end date'] = req.json()['data'][j]['to']

                # Combine with main df
                df_mix = pd.concat([df_mix, df], axis=0)

    # Extract data from JSON
    df_mix = df_mix.reset_index(drop = True)
    biomass, coal, imports, gas, nuclear, other, hydro, solar, wind = {}, {}, {}, {}, {}, {}, {}, {}, {}

    for i in df_mix.index:
        biomass.update({i: df_mix['generationmix'][i][0]['perc']})
        coal.update({i: df_mix['generationmix'][i][1]['perc']})
        imports.update({i: df_mix['generationmix'][i][2]['perc']})
        gas.update({i: df_mix['generationmix'][i][3]['perc']})
        nuclear.update({i: df_mix['generationmix'][i][4]['perc']})
        other.update({i: df_mix['generationmix'][i][5]['perc']})
        hydro.update({i: df_mix['generationmix'][i][6]['perc']})
        solar.update({i: df_mix['generationmix'][i][7]['perc']})
        wind.update({i: df_mix['generationmix'][i][8]['perc']})

    df_mix['biomass'] = df_mix.index.map(biomass)
    df_mix['coal'] = df_mix.index.map(coal)
    df_mix['imports'] = df_mix.index.map(imports)
    df_mix['gas'] = df_mix.index.map(gas)
    df_mix['nuclear'] = df_mix.index.map(nuclear)
    df_mix['other'] = df_mix.index.map(other)
    df_mix['hydro'] = df_mix.index.map(hydro)
    df_mix['solar'] = df_mix.index.map(solar)
    df_mix['wind'] = df_mix.index.map(wind) 

    for col in df_mix.columns:
        if col == 'generationmix':
            del df_mix[col]

    # Fix North Wales & Merseyside tag
    df_mix['shortname'] = ['North Wales and Merseyside' if i == 'North Wales & Merseyside' else i for i in df_mix['shortname']]

    return df_mix

if __name__ == '__main__':
    df = get_api_data(dt.date(2022,1,1), dt.date(2022,1,1))
    df.to_csv(r'data/CarbonData.csv')