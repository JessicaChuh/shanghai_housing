import streamlit as st
import pandas as pd
import numpy as np

st.title("Shanghai housing")



def user_house_info():
    #collect these info to put into model
    Size = st.number_input('How big is your apt?', min_value=10, step=1)
    N_bed = st.number_input('How many bedrooms?',min_value=1, step=1)
    N_bath = st.number_input('How many bathrooms?',min_value=1, step=1)

    if st.multiselect(
        'What amenities does your apt come with?',
        ['Floor Heating',
         'Pool',
         'Fitness Centers',
         ]
    ):

        st.subheader('Raw data')
        st.write()


if st.button('Check market price'):
    # print is visible in the server output, not in the page
    print('button clicked!')
    st.write('waiting for model to excute')
else:
    st.write('There can be different on the real price due to other conditions')

Real_price = st.number_input('How much are you paying for your apt?', min_value=3000, step=50)
