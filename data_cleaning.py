import pandas as pd
import numpy as np

def clean_data(data):

    data.rename(columns={'Pets Allowed\n\n                                                                                    \n                                                true':'Pets_allowed'},
               inplace=True)

    to_drop = ['Rooms','Good View',
           'Pets Allowed\n\n                                                                                    \n                                                false']
    data.drop(columns=to_drop, inplace=True)

    data['Size'] = data['Size'].replace(r"\D+", "", regex=True).astype(int)

    #Floor has some non-numerical values, set them to 0 and convert it all to int
    data['Floor'] = pd.to_numeric(data['Floor'], errors='coerce', downcast='integer').fillna(0)

    # define regular expression pattern to match the different formats
    pattern = r'(?:First Posted\s+)?(\w+\s+\d+)'
    # extract month and day information as a string in the format 'Month day'
    data['First_post'] = pd.to_datetime(data['First_post'].str.extract(pattern, expand=False), format='%B %d').dt.strftime('2023-%m-%d')

    #for all the availabilities, if it's from now then change it to first post day, the rest remain unchanged.
    data.loc[data['Available From'] == 'Available Now', 'Available From'] = data.loc[data['Available From'] == 'Available Now', 'First_post']
    data['Available From'] = pd.to_datetime(data['Available From'], errors='coerce')


    #during the process of scraping data I got these 2 wrong
    data.rename(columns={'Longtitude':'Latitude','Latitude':'Longtitude'}, inplace=True)

    #we will drop some ourliers such as price over 60k, cause I can't afford it
    data.drop(index=data[data.Price > 60000].index, inplace=True)
    #some agent can't tell the difference bewteen price and size, let's drop them too
    data.drop(index=data[data.Size > 1000].index, inplace=True)
    #for some reason this agent is posting same apartment with all different price, let's just ignor all his listing
    data.drop(index=data[data.Agent == 'jdc107'].index, inplace=True)
    #for those have less less than 1 bedroom and bathrooms
    to_remove = data[data.N_Bedrooms < 1].index.to_list() + data[data.N_Bathrooms < 1].index.to_list()
    data.drop(index=to_remove, inplace=True)
    data.drop(index=data[data.Longtitude < 121].index, inplace=True)
    data.drop(index=data[data.Latitude > 31.4].index, inplace=True)
    # for those has different "Furniture" context
    data.drop(index=[7696,19276],inplace=True)

    #will find a way to deal with these columns later
    data.drop(columns=['Agency Commission',
                   'Main Window Facing', 'Area',
                   'Compound','Agent', 'Description', 'Refresh','Type'], inplace=True)
    data.Furnished.replace('-', 'Unfurnished',inplace=True)
    data.Pets_allowed.fillna(0,inplace=True)
    data.drop(index=data[data.Metro.isna()].index, inplace=True)
    data = data.reset_index(drop=True)
    return data
