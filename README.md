## **Analytics Engineering**
---

### **Carbon App**

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


### **Data Engineering - Rainfall Pipeline & Analytics App**

---

In this project I have developed a data pipeline which extracts monthly rainfall totals for >250 stations across Scotland. 

The pipeline has been deployed using Github actions, and two analytical solutions have also been deployed (further details below).

---

**Back End** - automated API extraction pipeline developed in Python & deployed via GitHub actions

- The SEPA_pipeline.py and the API_Extract.yml files are configured so as data/SEPA_Monthly.csv is updated once per month. 

- The souce of the update is the [SEPA Rainfall API](https://www2.sepa.org.uk/rainfall/DataDownload) which provides daily data for >250 measuring locations across Scotland. 

---

**Front End** - Data analytics app using Python (Streamlit / Pandas)

- There is a [streamlit app](https://share.streamlit.io/idataengineer/dataeng-rainfallapp/main/RainApp.py) attached to the backend dataset.The app maps all the stations and allows users to filter by station and by date. 

- The app provides insight into graphical trends and statistical summary.

- The app was featured in a streamlit weekly roundup in Jan-2022.

---

**Front End...Part 2** - Data analytics using power BI
    
- In the repo there is a powerBI folder, within which there is a power BI desktop file that is connected to SEPA_Monthly.csv.
    
- At the last update this front end is similar to what has been deployed to the streamlit app.

---

**Pipeline status** 

[![API_Extract](https://github.com/sciDelta/API-ETL-SEPA-rainfall/actions/workflows/API_Extract.yml/badge.svg)](https://github.com/sciDelta/API-ETL-SEPA-rainfall/actions/workflows/API_Extract.yml)

---

**Languages:** Python 3.9.10, YAML, DAX

---

**Tools:** Pandas 1.2.2, Streamlit 1.3.1, GitHub Actions, MS Power BI Desktop 2.1
