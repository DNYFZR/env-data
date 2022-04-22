**Data Engineering - Rainfall Pipeline, App & Analytics**

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
