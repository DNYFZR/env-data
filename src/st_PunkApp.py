# Punk App 
import requests, PIL, pandas as pd, streamlit as st
from io import BytesIO
from PunkPipeline import pipeline

@st.cache
def scale_image(image_url, new_width = 50):
    # get from web
    req = requests.get(image_url).content
    image_req = BytesIO(req)    
    
    # format image
    img = PIL.Image.open(image_req)
    wpercent = (new_width/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    
    return img.resize((new_width,hsize), PIL.Image.ANTIALIAS)


### Functions ###

@st.cache()
def get_data():
    return pipeline()

# App data set & filter lists
data = get_data()
names = data['name'].copy().sort_values().unique()


### App ###
st.title('🍻 BrewDog Punk API 🍻')

# filter dataset
select_name = st.sidebar.selectbox(label='Select Beer 🍻', options=names)
select_index = data[data['name'] == select_name].index

select_tagline = data.loc[select_index, 'tagline'].unique()[0]
select_image = data.loc[select_index, 'image_url'].unique()[0]
select_first_brew =  data.loc[select_index, 'first_brewed'].unique()[0]
select_food_pairs = data.loc[select_index, 'food_pairing']

# display output
col1, col2 = st.columns(2)

with col1:
    st.subheader(f'{select_name}')
    st.markdown(f'{select_tagline}')
    st.markdown(f'First Brewed: {select_first_brew}')
    st.markdown('''
    This is for adding stuff...
    
    ''')

    st.dataframe({k: v for k, v in enumerate(select_food_pairs)})
with col2:
    st.image(scale_image(select_image, new_width=100), output_format='PNG')



# Dataset check
st.dataframe(data) 