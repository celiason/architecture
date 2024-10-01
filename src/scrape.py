# Working version
# I got tips here- https://ahy3nz.github.io/fastpayges/personal/data%20science/2021/08/15/scrape-redfin1.html

from redfin import Redfin
import urllib.request
import time
import random
import pandas as pd
import os
import re
from tqdm import tqdm
import matplotlib.pyplot as plt

# TODO: extend to other cities?
# TODO add progress bar!
# TODO: figure out how to add these images to the dataset

# testing only-
# address = "613 S Grove Ave"

# setup redfin client
client = Redfin()

# function to get an image from a redfin listing
def get_redfin_image(address):

    input_address = address

    # search for the address    
    response = client.search(address + ", Oak Park")
    
    # TODO clean up these annotations

    if response['payload']['sections'][0]['rows'][0]['id'] == '23_null':
        
        # remove cardinal directions
        address = re.sub(r'\s[NSEW]\.*\s', ' ', address)
        response = client.search(address + ", Oak Park")

    
    try:
        # check if address has an exact match on Redfin
        url = response['payload']['exactMatch']['url']
        rf_address = response['payload']['exactMatch']['name']
    
    except:    
        # if not, take the first suggested match
        try: 
            url = response['payload']['sections'][0]['rows'][0]['url']
            rf_address = response['payload']['sections'][0]['rows'][0]['name']        
        # if there are no matches, return an error
        except:
            metadata = {
                'input': [input_address],
                'match': [''],
                'property_id': [''],
                'latitude': [float('nan')],
                'longitude': [float('nan')],
                'search_url': [''],
                'image_url': ['']
            }
            
            df = pd.DataFrame(metadata)
            
            # output empty data frame
            return df

    # get info on the listing
    initial_info = client.initial_info(url)
    
    # get the image URL
    img = initial_info['payload']['preloadImageUrls']
    
    # extract IDs for later
    pid = str(initial_info['payload']['propertyId'])

    # get other metadata (estimated price, etc.)
    try:
        cost = client.cost_of_home_ownership(property_id=pid)['payload']['homeValue']
    except:
        cost = float('nan')

    # TODO get other metadata!
    latlon = initial_info['payload']['latLong']

    metadata = {
        'input': [input_address],
        'match': [rf_address],
        'property_id': [pid],
        'latitude': [latlon['latitude']],
        'longitude': [latlon['longitude']],
        'search_url': [url],
        'image_url': [img],
        'home_value': [cost]
    }

    # TODO figure this out
    # client.descriptive_paragraph(url,lid)

    # put into a dataframe
    df = pd.DataFrame(metadata)

    file_address = rf_address.replace(' ', '-')

    # Download the image from the URL and save it as a file
    image_url = img[0]
    file_name = "../images/testing/" + file_address + "_pid" + pid + ".jpg"
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    
    urllib.request.urlretrieve(image_url, file_name)

    return df

# list of addresses in Cook county - found on the cookcountyil.gov website
cook = pd.read_csv("../data/raw/Assessor_-_Parcel_Addresses_20240910.csv")

# get unique addresses
unique_addresses = set(cook['mailing_address'])

# convert to string
unique_addresses = [str(x) for x in unique_addresses]

# number of unique addresses
len(unique_addresses) # 5305

# Initialize an empty DataFrame to store metadata
metadata_df = pd.DataFrame()

# Range of indices to run the search through
idx = range(len(unique_addresses))  # all addresses

# Get images for all addresses
for i in tqdm(idx, desc="Processing addresses"):
    # Query address
    address = unique_addresses[i]
    try:
        # Get the metadata for the address
        df = get_redfin_image(address)
        # Append to metadata DataFrame
        metadata_df = pd.concat([metadata_df, df], ignore_index=True)
    except:
        continue
    # Add a random sleep time between 1 to 3 seconds
    time.sleep(random.uniform(1, 3))

# Save the metadata to a CSV file
metadata_df.to_csv('../data/interim/redfin_metadata.csv', index=False)

# Debugging stuff

# Histogram of home values
# metadata_df.hist(column='home_value', bins=100)

# Get the index of a given address (useful for debugging)
# unique_addresses.index('816 S MAPLE AVE APT 2S')

# idx = range(2867, len(unique_addresses))  # subset of addresses - "debugging mode"

