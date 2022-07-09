# **ENVRMNT APP**

Cloud hosted Stremlit Data analytics app operating with two data access structures - a live API connection & a maintained dataset.

| **Component** | **Status**
|--|--
| Streamlit App | [![ENVRMNT APP](https://img.shields.io/badge/Streamlit-Live-brightgreen?icon=github)](https://dnyfzr-env-data-srcenviro-app-qeoqz3.streamlitapp.com/)
| Data Pipeline | [![Data Pipeline](https://github.com/iDataEngineer/Analytics-Engineering/actions/workflows/pipeline_rainfall_monthly.yml/badge.svg)](https://github.com/iDataEngineer/Analytics-Engineering/actions/workflows/pipeline_rainfall_monthly.yml)

---

## **Carbon Intensity**

This data pipeline extracts data from the National [Grid Carbon Intensity API](https://carbon-intensity.github.io/api-definitions/#carbon-intensity-api-v2-0-0), which is then into a streamlit app.

The CI part of app allows users to select a date range and the DNO area (network operator) of interest. Available areas include Great Britain, England, Scotland, Wales and the 14 network operator areas - Scotland is made up of a North DNO and a South DNO.

---

## **Rainfall API & Database**

This data pipeline, deployed using Github actions, extracts monthly rainfall totals for >250 stations across Scotland.


Automated API extraction pipeline developed in Python & deployed via GitHub actions

---

**Languages / Tools**

- Carbon Intensity : [requirements file](req/req_carbon_app.txt) for this app.
- Rainfall : [requirements file](req/req_rain_app.txt) for this app.

**Scripts**

pipeline_carbon.py

- Takes the selected date range as an input.
- Returns the half hourly data from the API in a pandas dataframe.


pipeline_rainfall.py

- Extracts monthly data from the API and updates the stored dataset

pipeline_rainfall_monthly.yml 

- The script which orchestrates the GitHub Actions run

---
