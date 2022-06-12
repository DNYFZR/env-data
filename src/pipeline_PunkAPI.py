# Punk API Data Pipeline
'''
Extracts all data from the Brewdog Punk API and returns a data frame with the combined outputs 
'''
import requests, pandas as pd

# Data Pipeline
def pipeline(url = 'https://api.punkapi.com/v2/beers?page={}&per_page=80', pages = 50):
    output_data = dict()

    # iterate over API pages
    for page in range(1, pages + 1):
        api = requests.get(url.format(page)).json()
        
        if len(api) == 0:
            pass
        
        else:
            # first brewed date
            for i in range(len(api)):
                api[i]['first_brewed'] = pd.to_datetime(api[i]['first_brewed']).date()

            # volume in litres
                if type(api[i]['volume']) != int:
                    api[i]['volume'] = api[i]['volume']['value']

            # boil volume in litres
                if type(api[i]['boil_volume']) != int:
                    api[i]['boil_volume'] = api[i]['boil_volume']['value']        

            # method JSON to new cols
            for i in range(len(api)):
                if 'method' in api[i].keys():
                    
                    # mash_temp - extract temp value & duration
                    if 'mash_temp' in api[i]['method']:
                        api[i]['mash_duration_mins'] = api[i]['method']['mash_temp'][0]['duration']  
                        api[i]['mash_temp_degC'] = api[i]['method']['mash_temp'][0]['temp']['value']
                        api[i]['method'].pop('mash_temp')

                    # fermentation - temp value only
                    if 'fermentation' in api[i]['method'] and type(api[i]['method']['fermentation']) != int:
                        api[i]['fermentation_temp_degC'] = api[i]['method']['fermentation']['temp']['value']
                        api[i]['method'].pop('fermentation')

                    # twist - extract string for now 
                    if 'twist' in api[i]['method']:
                        api[i]['twist'] = api[i]['method']['twist']
                        api[i]['method'].pop('twist')

                    # remove method col
                    api[i].pop('method')

            # ingredients JSON to upper level
            for i in range(len(api)):
                if 'ingredients' in api[i].keys():
                    api[i]['ingredients_malt'] = api[i]['ingredients']['malt']
                    api[i]['ingredients_hops'] = api[i]['ingredients']['hops']
                    api[i]['ingredients_yeast'] = api[i]['ingredients']['yeast']

                    api[i].pop('ingredients')

            # ingredients_malt clean
            for i in range(len(api)):
                line_data = {}
                for j in range(len(api[i]['ingredients_malt'])):
                    name = api[i]['ingredients_malt'][j]['name']
                    val = api[i]['ingredients_malt'][j]['amount']['value']
                    line_data.update({name : val})
                api[i]['ingredients_malt'] = line_data
        
            # ingredients_hops clean 
            for i in range(len(api)):
                temp_list = list()
                for j in api[i]['ingredients_hops']:
                    temp = list()
                    temp.append(j['name'])
                    temp.append(str(j['amount']['value']) + 'g')
                    temp.append(j['add'])
                    temp.append(j['attribute'])
                    temp_list.append(temp)

                api[i]['ingredients_hops'] = temp_list

            # update overall dataset
            current_len = len(output_data)
            for i in range(len(api)):
                api[i].pop('id')
                api[i].pop('contributed_by')
                
                output_data[current_len + i] = api[i]

    return pd.DataFrame(data = output_data.values(), index = output_data.keys())

# function test
if __name__ == '__main__':
    import datetime as dt, time
    start = time.time()
    run_date = dt.datetime.today().strftime('%Y-%m-%d')

    punk_api = pipeline()
    print('Runtime:', time.time() - start, 's')
    punk_api.to_csv(f'data/Punk API Data run {run_date}.csv', index = None)