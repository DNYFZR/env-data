__SEPA Rainfall API ELT__
---

Pipeline pulling the daily and monthly rainfall data from 300 monitoring stations via a SEPA API.  

__Files:__
1. SEPA_API_ETL.py - Python file for the ETL process.
2. SEPA_daily_rainfall_data.csv - output file - 12 months data to 30/05/21.
3. SEPA_monthly_rainfall_data.csv - output file - figures from at furthest 2011 on, some stations were not providing data for the full duration.
4. SEPA_station_info.csv - output file - API data for each station including name, id and lat / long co-ordinates. 
