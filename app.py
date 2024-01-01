import streamlit as st
import pandas as pd
import numpy as np
import joblib

model = joblib.load('random_forest_model.joblib')
frame = pd.read_csv('frame.csv')

def main():
    # User inputs
    # Number inputs
    size = st.number_input("Size")
    n_bedrooms = st.number_input("Number of Bedrooms")
    n_bathrooms = st.number_input("Number of Bathrooms")
    floor = st.number_input("Floor")

    # lower text inputs
    district = st.text_input("District").lower()
    metro = st.text_input("Metro").lower()

    # Checkbox inputs
    furnished = st.checkbox("Furnished")
    balcony = st.checkbox("Balcony")
    oven = st.checkbox("Oven")
    recently_renovated = st.checkbox("Recently Renovated")
    air_filter = st.checkbox("Air Filter")
    fitness_centers = st.checkbox("Fitness Centers")
    floor_heating = st.checkbox("Floor Heating")
    garden = st.checkbox("Garden")
    historic_building = st.checkbox("Historic Building")
    large_storage_room = st.checkbox("Large Storage Room")
    parking = st.checkbox("Parking")
    playground = st.checkbox("Playground")
    pool = st.checkbox("Pool")
    tennis_courts = st.checkbox("Tennis Courts")
    wall_heating = st.checkbox("Wall Heating")
    water_filter = st.checkbox("Water Filter")
    pets_allowed = st.checkbox("Pets Allowed")


    # Submit button
    if st.button("Submit"):
        # Create a dictionary to store the user input
        user_input = {
            'Size': size,
            'N_Bedrooms': n_bedrooms,
            'N_Bathrooms': n_bathrooms,
            'Floor': floor,
            'Furnished': int(furnished),
            'District': district,
            'Metro': metro,
            'Balcony': int(balcony),
            'Oven': int(oven),
            'Recently renovated': int(recently_renovated),
            'Air Filter': int(air_filter),
            'Fitness Centers': int(fitness_centers),
            'Floor Heating': int(floor_heating),
            'Garden': int(garden),
            'Historic Building': int(historic_building),
            'Large Storage Room': int(large_storage_room),
            'Parking': int(parking),
            'Playground': int(playground),
            'Pool': int(pool),
            'Tennis Courts': int(tennis_courts),
            'Wall heating': int(wall_heating),
            'Water Filter': int(water_filter),
            'Pets_allowed': int(pets_allowed)
        }


        # Create a DataFrame with the processed input
        input_df = pd.DataFrame(user_input, index=[0])
        frame[['Size', 'N_Bedrooms', 'N_Bathrooms', 'Floor', 'Furnished',
                'Balcony', 'Oven', 'Recently renovated', 'Air Filter',
                'Fitness Centers']] = input_df[['Size', 'N_Bedrooms', 'N_Bathrooms', 'Floor', 'Furnished', 'Balcony',
            'Oven', 'Recently renovated', 'Air Filter', 'Fitness Centers']]

        district = "District_" + input_df['District']
        metro = "Metro_" + input_df['Metro']
        frame[district] = 1
        frame[metro] = 1


        # Make the prediction
        prediction = model.predict(frame)[0]


        # Display the prediction
        st.write("Predicted House Price:")
        st.write(prediction)

if __name__ == '__main__':
    main()
