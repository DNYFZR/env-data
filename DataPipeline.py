#### Carbon Intensity API Pipeline ####
def get_api_data(start_date, end_date):
    import requests, pandas as pd, datetime as dt

    def date_list(start, end, interval):
        date_list = list()

        if start == end:
            date_list.append( (str(start), str(end + dt.timedelta(days = interval)) ) )
        
        else:
            i = start
            while i < end:
                first = i
                last = i + dt.timedelta(days = interval) 
                date_list.append( (str(first), str(last)) )
                i += dt.timedelta(days = interval)
        return date_list

    # NatGrid Carbon Intensity UK Regions API
    api_url = 'https://api.carbonintensity.org.uk/regional/intensity/{}T00:30Z/{}T00:00Z'
    headers = {'Accept': 'application/json'}
    df_mix = pd.DataFrame()

    api_date = date_list(start = start_date, end = end_date, interval = 1)

    # test
    for i, tup in enumerate(api_date):
        req = requests.get(api_url.format(api_date[i][0], api_date[i][1]), params={}, headers = headers)

        # Pandas DataFrame
        for j in range(48):
            if len(req.json()['data']) <= j:
                pass
            else:
                df = pd.DataFrame(req.json()['data'][j]['regions'])
                df['intensity'] = [i['forecast'] for i in df['intensity']]

                # Start & end timestamps
                df['start date'] = pd.to_datetime(req.json()['data'][j]['from'])
                df['end date'] = pd.to_datetime(req.json()['data'][j]['to'])

                # Combine with main df
                df_mix = pd.concat([df_mix, df], axis=0)

    # Extract generation mix data
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

    # dates
    df_mix['start date'] = df_mix['start date'].dt.strftime('%Y-%m-%d %H:%M')
    df_mix['end date'] = df_mix['end date'].dt.strftime('%Y-%m-%d %H:%M')

    # Fix North Wales & Merseyside tag
    df_mix['shortname'] = ['North Wales and Merseyside' if i == 'North Wales & Merseyside' else i for i in df_mix['shortname']]

    return df_mix