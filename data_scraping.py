import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

baseurl = 'https://www.smartshanghai.com/housing/apartments-rent'
house_data = pd.read_csv("housing_data_full.csv",low_memory=False)

def get_data(a,b):
    contents = []
    for page in range(a,b):

        params = {'page': page}
        response = requests.get(baseurl,params)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            contents.append(soup.find_all("div", class_ = 'cont'))

        else:
            print(response.status_code)
    return contents

def extract_data(contents):

    Listing_Id = []
    District = []
    Price = []
    Size = []
    N_Bedrooms = []
    N_Bathrooms = []

    for content in contents:
        for i in range(len(content)):
            Listing_Id.append(content[i].find('div').attrs['data-listingid'])

            apts = content[i].find('div', class_ = 'body')
            price = apts.find('div', class_ = 'price').text.strip().split()[1].split(',')
            Price.append(price[0]+price[1])

            info = re.findall('\d+', apts.find('div', class_ = 'room-type').text.strip())
            Size.append(info[0])
            N_Bedrooms.append(info[1])
            N_Bathrooms.append(info[2])

    df = pd.DataFrame(np.column_stack([Listing_Id,Price,Size,N_Bedrooms,N_Bathrooms]),
                    columns=['Listing_Id','Price','Size','N_Bedrooms', 'N_Bathrooms'])

    return df
    #return pd.concat((house_data, df), ignore_index=True)


def page_data(data):

    features = ['Type', 'Available From', 'Agency Commission', 'Rooms', 'Size',
               'Floor', 'Furnished', 'Main Window Facing', 'District', 'Area',
                'Compound', 'Metro Station', 'Longtitue', 'Latitude', 'posting agent', 'description', 'first_post', 'Refresh']


    for list_id in data.Listing_Id:
        response = requests.get(f'{baseurl}/{list_id}')
        if response.status_code == 200:
            soup_info = BeautifulSoup(response.content, "html.parser")


        #each list's information
        try:
            detail = soup_info.find_all('div', class_='details')[0].find_all(name='div')
        except IndexError:
            print(list_id)

        #from 'Type' to 'Area'
        for indx, j in enumerate(detail[0:-3]):
            house_data.loc[list_id,features[indx]] = j.text.strip()

        #'Compound'
        house_data.loc[list_id,"Compound"] = detail[-3].text.split('/')[0].strip()

        # metro station
        text = detail[-2].text
        try:
            found = re.search('walk to(.+?)on line', text).group(1)
        except AttributeError:
            found = ''
        house_data.loc[list_id,"Metro"] = found.strip()

        #long & lat
        long = soup_info.find('span', itemprop="longitude").text
        lat = soup_info.find('span', itemprop="latitude").text
        house_data.loc[list_id,"Longtitude"] = long
        house_data.loc[list_id,"Latitude"] = lat

        #posting agent
        house_data.loc[list_id,"Agent"] = soup_info.find('p', class_='username').text

        #description
        house_data.loc[list_id,"Description"] = soup_info.find('div', class_='description').text.strip()

        #post and views
        post = soup_info.find('div', class_='posted-and-views').text.strip().split(',')

        house_data.loc[list_id,"First_post"] = ' '.join(post[0].split(' ')[1:])
        house_data.loc[list_id,"Refresh"] = ' '.join(post[2].split(' ')[2:])

        #values.append(value)  # all listings

        #amenities
        amenity_pos = soup_info.find('div', class_='amenities').find_all('li', class_='positive')
        amenity_neg = soup_info.find('div', class_='amenities').find_all('li', class_='negative')

        amenity_pos = [i.text.strip() for i in amenity_pos]
        amenity_neg = [i.text.strip() for i in amenity_neg]

        for indx, amenity in enumerate(amenity_pos):
            house_data.loc[list_id,amenity_pos[indx]] = 1

        for indx, amenity in enumerate(amenity_neg):
            house_data.loc[list_id, amenity_neg[indx]] = 0
    return house_data

def save_data():
    house_data = extract_data(get_data(0,25))
    house_data = house_data.drop_duplicates()
    to_page = house_data[house_data['Type'].isnull()]

    house_data["extra_index"] = house_data.Listing_Id
    house_data.set_index("extra_index", inplace=True)

    house_data = page_data(to_page)
    #house_data.to_csv("housing_data_full.csv", index=False)
    print(f"Done, current size of database is {house_data.shape}")
    return house_data
