import schedule
import time
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
from config import baseurl

current_time = datetime.now()

# Function to convert time indicator to a timedelta
def convert_time_indicator(time_str):
    time_value = int(time_str.split()[0])

    if 'minute' in time_str:
        return timedelta(minutes=time_value)
    elif 'hour' in time_str:
        return timedelta(hours=time_value)
    elif 'day' in time_str:
        return timedelta(days=time_value)
    elif 'week' in time_str:
        return timedelta(weeks=time_value)
    elif 'month' in time_str:
        return timedelta(days=time_value * 30)  # Assuming a month is 30 days

    return timedelta()

# Function to extract listing IDs posted within the last 7 days
def get_recent_listing_ids():
    Listing_id = []
    Price = []
    N_Bedrooms = []
    N_Bathrooms = []
    page = 0
    while True:
        params = {'page': page}
        response = requests.get(baseurl, params)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            content = soup.find_all("div", class_='cont')

            if not content:  # Stop if there are no more listings
                break

            for i in range(len(content)):
                listing_time_element = content[i].find('div', class_='address').text.strip()
                time_diff = convert_time_indicator(listing_time_element)

                if time_diff <= timedelta(hours=1):
                    Listing_id.append(content[i].find('div').attrs['data-listingid'])
                    Price.append(''.join(content[i].find('div', class_="price").text.strip().split()[1].split(',')))
                    info = re.findall('\d+', content[i].find('div', class_='room-type').text.strip())
                    N_Bedrooms.append(info[1])
                    N_Bathrooms.append(info[2])
                else:
                    # Stop scraping when encountering a listing older than 7 days
                    return pd.DataFrame({'listing_id': Listing_id, 'price': Price, 'N_Bedrooms': N_Bedrooms, 'N_Bathrooms': N_Bathrooms})

            page += 1
        else:
            print(response.status_code)
            break

    return pd.DataFrame({'listing_id': Listing_id, 'price': Price, 'N_Bedrooms': N_Bedrooms, 'N_Bathrooms': N_Bathrooms})




daily_data = get_recent_listing_ids()
daily_data = daily_data.drop_duplicates().reset_index(drop=True)

columns = []
values = []
amenities_data = []
views_data = []

for list_id in daily_data['listing_id']:
    response = requests.get(f'{baseurl}/{list_id}')

    if response.status_code == 200:
        soup_info = BeautifulSoup(response.content, "html.parser")

        # Extract the labels and values for the current listing ID
        labels = [label.get_text(strip=True)[:-1] for label in soup_info.find_all('div', class_='details')[0].find_all(name='label')]
        row_values = [value.get_text(strip=True) for value in soup_info.find_all('div', class_='details')[0].find_all(name='div')[:-1]]
        labels.extend(['lat','long'])
        row_values.extend([soup_info.find('span', itemprop="longitude").text,soup_info.find('span', itemprop="latitude").text])

        # Append unique columns to the columns list
        columns.extend(label for label in labels if label not in columns)

        # Append values for the current listing ID while maintaining the correct order
        row = {}
        for label, value in zip(labels, row_values):
            row[label] = value
        values.append(row)

        # Extract amenities information
        amenities = soup_info.find_all('div', class_='amenities')[0].find_all('li', class_=['positive', 'negative'])
        amenities_dict = {}

        for amenity_li in amenities:
            amenity = amenity_li.text.strip()
            amenities_dict[amenity] = 1 if 'positive' in amenity_li['class'] else 0

        amenities_dict['listing_id'] = list_id
        amenities_data.append(amenities_dict)

        # Extract views information
        views = re.findall('\d+', soup_info.find('div', class_="posted-and-views").text.split('·')[-1])[0]
        views_data.append({'listing_id': list_id, 'views': views})

    else:
        print(f"Failed to retrieve data for listing ID: {list_id}")

# Create DataFrames for values, amenities, and views data
values_df = pd.DataFrame(values)
amenities_df = pd.DataFrame(amenities_data)
views_df = pd.DataFrame(views_data)

# Merge the amenities DataFrame with the original DataFrame on 'listing_id'
merged_df = pd.merge(daily_data, amenities_df, on='listing_id', how='left')

# Merge the views DataFrame with the merged DataFrame on 'listing_id'
merged_df = pd.merge(merged_df, views_df, on='listing_id', how='left')

# Concatenate the merged DataFrame with the values DataFrame
final_df = pd.concat([merged_df, values_df], axis=1)
final_df.columns = final_df.columns.str.replace("\n", "").str.replace(" ", "")


#Data cleaning
final_df.columns = final_df.columns.str.replace("\n", "").str.replace(" ", "")

# List of columns to clean
columns_to_clean = ['MinimalRentalPeriod', 'DepositRequirement', 'AdvanceRentPayment','AgencyCommission','Size']

# Define a function to clean the data in each specified column
def clean_column_data(df, column):
    df[column] = df[column].str.extract('(\d+)')

# Apply the cleaning operation to each column in the list
for column in columns_to_clean:
    clean_column_data(final_df, column)

final_df['MetroStation'] = final_df['MetroStation'].str.split('to').str[1].str.split('on ').str[0].str.strip()

# Keep only 'PetsAllowedtrue' column and rename it to 'PetsAllowed'
final_df['PetsAllowed'] = final_df['PetsAllowedtrue']

# Drop 'PetsAllowedtrue' column
final_df.drop(columns=['PetsAllowedtrue','Rooms'], inplace=True)

# Fill NaN values in the 'PetsAllowed' column with 0
final_df['PetsAllowed'] = final_df['PetsAllowed'].fillna(0)
final_df = final_df.fillna(0)

final_df.to_csv(f"{current_time.strftime('%Y%m%d')}.csv", index=False)
