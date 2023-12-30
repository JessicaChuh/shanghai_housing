import streamlit as st
import pandas as pd
import numpy as np
import joblib

model = joblib.load('random_forest_model.joblib')
metro_encoder = joblib.load('metro_encoder.joblib')
district_encoder = joblib.load('district_encoder.joblib')

def main():
    # User inputs
    district = st.text_input("District", "")
    metro = st.text_input("Metro", "")
    balcony = st.checkbox("Balcony")
    oven = st.checkbox("Oven")
    recently_renovated = st.checkbox("Recently renovated")
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
    wall_heating = st.checkbox("Wall heating")
    water_filter = st.checkbox("Water Filter")
    pets_allowed = st.checkbox("Pets Allowed")

    # Process user input using the encoders
    district_encoded = district_encoder.transform([[district]])
    metro_encoded = metro_encoder.transform([[metro]])

    # Create a DataFrame with the processed input
    input_data = pd.DataFrame(data=district_encoded, columns=district_encoder.get_feature_names_out(['District']))
    input_data = pd.concat([input_data, pd.DataFrame(data=metro_encoded, columns=metro_encoder.get_feature_names_out(['Metro']))], axis=1)

    # Add additional user inputs to the DataFrame
    input_data['Balcony'] = int(balcony)
    input_data['Oven'] = int(oven)
    input_data['Recently_renovated'] = int(recently_renovated)
    input_data['Air_Filter'] = int(air_filter)
    input_data['Fitness_Centers'] = int(fitness_centers)
    input_data['Floor_Heating'] = int(floor_heating)
    input_data['Garden'] = int(garden)
    input_data['Historic_Building'] = int(historic_building)
    input_data['Large_Storage_Room'] = int(large_storage_room)
    input_data['Parking'] = int(parking)
    input_data['Playground'] = int(playground)
    input_data['Pool'] = int(pool)
    input_data['Tennis_Courts'] = int(tennis_courts)
    input_data['Wall_Heating'] = int(wall_heating)
    input_data['Water_Filter'] = int(water_filter)
    input_data['Pets_Allowed'] = int(pets_allowed)

    # Make the prediction
    prediction = model.predict(input_data)

    # Display the prediction
    st.write("Predicted House Price:")
    st.write(prediction)

if __name__ == '__main__':
    main()
