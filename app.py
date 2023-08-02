import streamlit as st
import pandas as pd
import numpy as np

st.title("Shanghai housing")

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache_data)")

def user_house_info():
    #collect these info to put into model
    Size = st.number_input('How big is your apt?')
    N_bed = st.number_input('How many bedrooms?')
    N_bath = st.number_input('How many bathrooms?')

    if st.checkbox('Floor heating'):
        st.subheader('Raw data')
        st.write(data)


if st.button('Check market price'):
    # print is visible in the server output, not in the page
    print('button clicked!')
    st.write('waiting for model to excute')
else:
    st.write('There can be different on the real price due to other conditions')
