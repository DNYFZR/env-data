''' NASA Earth Observatory Natural Event API Pipeline '''
import requests, pandas as pd

def earth_event_pipeline(api_url = 'https://eonet.gsfc.nasa.gov/api/v3/events'):
    '''
    This fucntion works with the JSON API output from the NASA Earth Observatory Natural Events Tracker
    Dependencies: Python 3.9.10 w/ pandas, requests
    '''

    # Extract - API JSON contains keys: 'title', 'description', 'link', 'events' - 'events' contains all the data
    dataset = requests.get(api_url).json()['events']

    # Transform
    for i in dataset:
        nation = i['title'].split(' - ')[-1]
        # some events have more info in the nation section of the title
        try:
            nation.split(', ')[-1]
        except IndexError:
            i['nation'] = nation
        else:
            i['nation'] = nation.split(', ')[-1]

        # take the single category type
        i['categories'] = i['categories'][0]['title']
        
        # keep only source url
        i['sources'] = i['sources'][0]['url']
        
        # split out magnitude val & unit
        i['magnitude'] = i['geometry'][0]['magnitudeValue']
        if i['magnitude'] is not None:
            i['magnitude'] = float(i['magnitude'])

        i['mag_unit'] = i['geometry'][0]['magnitudeUnit']
        
        # Extract & format event date
        i['event_date'] = pd.to_datetime(i['geometry'][0]['date'])
        
        # Extract geometric data
        i['geometry_type'] = i['geometry'][0]['type']
        i['latitude'] = float(i['geometry'][0]['coordinates'][1]) 
        i['longitude'] = float(i['geometry'][0]['coordinates'][0])

        # delete holding key in JSON
        del i['geometry']

    return pd.DataFrame(dataset)

if __name__ == '__main__':
    data = earth_event_pipeline()