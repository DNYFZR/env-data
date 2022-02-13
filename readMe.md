**SEPA Rainfall API ETL**

---

| **Pipeline status**
|--
|[![API_Extract](https://github.com/sciDelta/API-ETL-SEPA-rainfall/actions/workflows/API_Extract.yml/badge.svg)](https://github.com/sciDelta/API-ETL-SEPA-rainfall/actions/workflows/API_Extract.yml)


**Languages:** Python 3.9.10, YAML

**Tools:** Pandas 1.2.2, GitHub Actions, Streamlit 1.3.1

This project consists of two main parts:

- **Back End** - automated API extraction using Python & GitHub Actions

    The SEPA_pipeline.py and the API_Extract.yml files are configured so as data/SEPA_Monthly.csv is updated once per month. 

    The souce of the update is the [SEPA Rainfall API](https://www2.sepa.org.uk/rainfall/DataDownload) which provides daily data for >250 measuring locations across Scotland. 

    The reason for this structure is simple - a colleague needed this csv file in this structure for their own process - and I wanted to have this process fully automated on my part. 

- **Front End** - Data analytics app using Python(Streamlit / Pandas)

    There is a [streamlit app](https://share.streamlit.io/idataengineer/dataeng-rainfallapp/main/RainApp.py) attached to the backend dataset.The app maps all the stations and allows users to filter by station and by date. 

    The app provides insight into graphical trends and statistical summary.

    The app was featured in a streamlit weekly roundup in Jan-2022.
