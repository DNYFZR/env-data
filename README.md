## **Analytics Engineering**

---

#### Apr / May 2022

---

I am currently merging a number of projects into a larger one.

The readMe below will be not completely accurate while this message is still present.

---

#### **Carbon App**

---

This data / analytics engineering project extracts data from the National [Grid Carbon Intensity API](https://carbon-intensity.github.io/api-definitions/#carbon-intensity-api-v2-0-0) through a data pipeline, and then into a streamlit app.

The app allows users to select a date range and the DNO area (network operator) of interest. Available areas include Great Britain, England, Scotland, Wales and the 14 network operator areas - Scotland is made up of a North DNO and a South DNO.

The output of the app is a trend of carbon intensity, the energy mix breakdown, summary stats and a pie chart for each of the 18 areas measured.

The streamlit app can be accessed here: [Carbon App](https://share.streamlit.io/idataengineer/dataeng-carbonapp/main/CarbonApp.py)

**Languages / Tools**

See [requirements file](req/req_carbon_app.txt) for this app.

**Scripts**

pipeline_carbon.py

- Takes the selected date range as an input.
- Returns the half hourly data from the API in a pandas dataframe.

st_CarbonApp.py

- Transforms the dataset and extracts summary statistics.
- Creates the streamlie app set up.

---


### **Data Engineering - Rainfall Pipeline & Analytics App**

---

In this project I have developed a data pipeline which extracts monthly rainfall totals for >250 stations across Scotland. 

The pipeline has been deployed using Github actions, and two analytical solutions have also been deployed (further details below).

**Back End** - automated API extraction pipeline developed in Python & deployed via GitHub actions

- The pipeline_rainfall.py and the pipeline_rainfall_monthly.yml files are configured so as data/RainfallData/SEPA_Monthly.csv is updated once per month. 

- The souce of the update is the [SEPA Rainfall API](https://www2.sepa.org.uk/rainfall/DataDownload) which provides daily data for >250 measuring locations across Scotland. 

**Front End** - Data analytics app using Python (Streamlit / Pandas)

- st_CarbonApp

- The app provides insight into graphical trends and statistical summary.

**Front End...Part 2** - Data analytics using [power BI](powerBI/PBI%20rainfall.pbix) - connected to SEPA_Monthly.csv.

**Pipeline status :** Work in progress...

**Languages / Tools : ** See [requirements file](req/req_rain_app.txt) for this app.

