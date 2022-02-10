**SEPA Rainfall API ELT**

---

In this project we extract data from a rainfall API. The API contains data on >250 stations from across Scotland. 

The scope of the project is to: 
- automatically extract data from the API over the required time period.
- clean and process this data into a usable format. 
- build an analytics front end to allow users to interact with and gain insights the data.

**Languages:** Python, YAML
**Tools:** Streamlit, Pandas, GitHub Actions

This data engineering project consists of two main parts:

- **Back End** - automated API extraction using Python & GitHub Actions
    The SEPA_pipeline.py and the API_Extract.yml files are configured so as data/SEPA_Monthly.csv is updated once per month. 

    The souce of the update is the [SEPA Rainfall API](https://www2.sepa.org.uk/rainfall/DataDownload) which provides daily data for >250 measuring locations across Scotland. 

    The reason for this structure is simple - a colleague needed this csv file in this structure for their own process - and I wanted to have this process fully automated on my part. 

- **Front End** - Data analytics app using Python(Streamlit / Pandas)
    There is a [streamlit app](https://share.streamlit.io/scidelta/api-etl-sepa-rainfall/main/RainApp.py) attached to the backend dataset.The app maps all the stations and allows users to filter by station and by date. 

    The app provides insight into graphical trends and statistical summary.

    The app was featured in a streamlit weekly roundup in Jan-2022.