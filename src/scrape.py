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

# check errors
# get_redfin_image(address = "1101 S CLARENCE AV") # OK works fine
# get_redfin_image(address = "555 LAUREL AVE #524") # OK returns None in DF


# function to get an image from a redfin listing
def get_redfin_image(address):

    input_address = address

    # search for the address    
    response = client.search(address + ", Oak Park")
    
    if response['payload']['sections'][0]['rows'][0]['id'] == '23_null':
        # remove cardinal directions
        address = re.sub(r'\s[NSEW]\.*\s', ' ', address)
        response = client.search(address + ", Oak Park")

    try:
        # check if it has an exact match
        url = response['payload']['exactMatch']['url']
        rf_address = response['payload']['exactMatch']['name']

    except:

        try:
            # if not, take the first suggested match
            url = response['payload']['sections'][0]['rows'][0]['url']
            rf_address = response['payload']['sections'][0]['rows'][0]['name']        

        except:
            # if there are no matches, return an error
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

    # TODO get other metadata!
    latlon = initial_info['payload']['latLong']

    metadata = {
        'input': [input_address],
        'match': [rf_address],
        'property_id': [pid],
        'latitude': [latlon['latitude']],
        'longitude': [latlon['longitude']],
        'search_url': [url],
        'image_url': [img]
    }

    # TODO figure this out
    # client.descriptive_paragraph(url,lid)

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
unique_addresses = [str(x) for x in unique_addresses]
len(unique_addresses) # 5305 unique addresses


# Initialize an empty DataFrame to store metadata
metadata_df = pd.DataFrame()

# get images for all addresses
for address in tqdm(unique_addresses, desc="Processing addresses"):
    df = get_redfin_image(address)
    metadata_df = pd.concat([metadata_df, df], ignore_index=True)
    # Add a random sleep time between 1 to 3 seconds
    time.sleep(random.uniform(1, 3))

# Save the metadata to a CSV file
metadata_df.to_csv('../data/interim/redfin_metadata.csv', index=False)

# NB: a common "problem" is that many listings have photos from google maps, so they return an error

# stopped this at address 603/5305, so I can test the images
# would've taken about 4 hours to run all 5305 addresses

