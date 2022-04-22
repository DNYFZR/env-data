---

#### Carbon App

---

This data / analytics engineering project extracts data from the National [Grid Carbon Intensity API](https://carbon-intensity.github.io/api-definitions/#carbon-intensity-api-v2-0-0) through a data pipeline, and then into a streamlit app.

The app allows users to select a date range and the DNO area (network operator) of interest. Available areas include Great Britain, England, Scotland, Wales and the 14 network operator areas - Scotland is made up of a North DNO and a South DNO.

The output of the app is a trend of carbon intensity, the energy mix breakdown, summary stats and a pie chart for each of the 18 areas measured.

The streamlit app can be accessed here: [Carbon App](https://share.streamlit.io/idataengineer/dataeng-carbonapp/main/CarbonApp.py)

---

**Languages / Tools**

---

- Python 3.9.10
- Requests 2.25.1
- Numpy 1.19.5
- Pandas 1.2.2
- Streamlit 1.3.1
- Matplotlib 3.4.2
- Seaborn 0.11.1

---

**Scripts**

---

DataPipeline.py

- Takes the selected date range as an input.
- Returns the half hourly data from the API in a pandas dataframe.

CarbonApp.py

- Transforms the dataset and extracts summary statistics.
- Creates the streamlie app set up.

---
