### Carbon Intensity API Data Pipeline ###
import requests, pandas as pd, datetime as dt

class carbon_data:
    def __init__(self, start_date, end_date):
        self.start = start_date
        self.end = end_date
        
        # extract data
        self.api_url ='https://api.carbonintensity.org.uk/regional/intensity/{}T00:30Z/{}T00:00Z'
        self.api_headers = {'Accept': 'application/json'}
        self.api_json = list()
        
        # load data
        self.output_table = pd.DataFrame()

        # transform data
        self.output = pd.DataFrame()


    def extract_data(self):
        '''
        Function calls the API url and returns the JSON data structure between teh selected dates
        '''
        # Create list of dates for URL
        date_list = list()

        if self.start == self.end:
            date_list.append( (str(self.start), str(self.end + dt.timedelta(days = 1)) ) )
        else:
            i = self.start
            while i < self.end:
                first = i        
                last = i + dt.timedelta(days = 1) 
                date_list.append( (str(first), str(last)) )
                i += dt.timedelta(days = 1)

        # Extract JSON from API and append to list
        for i in range(len(date_list)):
            url = self.api_url.format(date_list[i][0], date_list[i][1])
            req = requests.get(url, params={}, headers = self.api_headers).json()
            self.api_json.append(req)
        

    def load_data(self):
        # Set up columns
        start_dates, end_dates = list(), list()
        data_nest = list()

        # Extract dates from 1st level JSON
        for json_nest in self.api_json:
            json_nest = json_nest['data']

            [start_dates.append(i['from']) for i in json_nest]
            [end_dates.append(i['to']) for i in json_nest]
            [data_nest.append(i['regions']) for i in json_nest]

        # Create & update output table
        self.output_table['Start'] = [pd.to_datetime(i) for i in start_dates]
        self.output_table['End'] = [pd.to_datetime(i) for i in end_dates]
        self.output_table['data']  = data_nest
    
        
    def transform_data(self):
        # Set up containers      
        start, end, ids, names, intensity, energy = list(), list(), list(), list(), list(), list()

        # Transform data structure
        for row, data in enumerate(self.output_table['data'].copy()):
            start_date = self.output_table.loc[row, 'Start']
            end_date = self.output_table.loc[row, 'End']

            for region in data:
                start.append(start_date)
                end.append(end_date)
                ids.append(region['regionid'])
                names.append(region['shortname'])
                intensity.append(region['intensity']) 
                energy.append(region['generationmix']) 

        self.output['Start'] = start
        self.output['End'] = end
        self.output['ID'] = ids
        self.output['Name'] = names
        self.output['Intensity'] = [i['forecast'] for i in intensity]
        self.output['Intensity Category'] = [i['index'] for i in intensity]
        self.output['Energy Mix'] = energy
        

    def transform_energy(self):
        # Set up containers for energy mix extraction
        biomass, hydro, solar = list(), list(), list()
        
        wind, coal, gas = list(), list(), list()
        
        nuclear, imports, other = list(), list(), list()

        energy = self.output['Energy Mix'].copy()
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

        self.output['Biomass %'] = biomass
        self.output['Hydro %'] = hydro
        self.output['Solar %'] = solar
        self.output['Wind %'] = wind
        self.output['Coal %'] = coal
        self.output['Gas %'] = gas
        self.output['Nuclear %'] = nuclear
        self.output['Imports %'] = imports
        self.output['Other %'] = other
        del self.output['Energy Mix']
        

    def run_pipeline(self):
        self.extract_data()
        self.load_data()
        self.transform_data()
        self.transform_energy()
        
        return self.output

if __name__ == '__main__':
    from time import time
    run_start = time()
    
    start_date = dt.date(2022,1,1) 
    end_date = dt.date(2022,4,1)

    data = carbon_data(start_date, end_date)
    output = data.run_pipeline()

    print(f'Run time: {round(time() - run_start, 1)}s')