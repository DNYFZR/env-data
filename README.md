#### Analytics Engineering

This project extracts a feed from the National Grid carbon intensity API through a data pipeline, and then into a streamlit app. 

The app allows users to select a date range and the area of interest. Available areas include Great Britain, England, Scotland, Wales and the 14 network operator areas - Scotland is made up of a North DNO and a South DNO.

The output of the app is a trend of carbon intensity, the energy mix breakdown, summary stats and a pie chart for each of the 18 areas measured.

This project contains two main scripts:

- DataPipeline.py - this takes the selected dates and returns the raw half hourly data from the API in a dataframe.
- CarbonApp.py - this transforms the data and also creates the streamlie app. 

The streamlit app can be accessed here: https://t.co/h511FDLXBt