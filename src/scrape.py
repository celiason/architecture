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

    # store the input address since we'll be modifying it
    input_address = address

    # search for the address    
    response = client.search(address + ", Oak Park")
    
    # sometime a fuzzy input address will not return any matches
    # we can try removing the cardinal directions from the address
    if response['payload']['sections'][0]['rows'][0]['id'] == '23_null':
        address = re.sub(r'\s[NSEW]\.*\s', ' ', address)
        response = client.search(address + ", Oak Park")

    # check if address has an exact match on Redfin
    try:        
        url = response['payload']['exactMatch']['url']
        rf_address = response['payload']['exactMatch']['name']

    # if not, check if there are any fuzzy matches
    except:
        # take the first address 'hit' in the list
        try: 
            url = response['payload']['sections'][0]['rows'][0]['url']
            rf_address = response['payload']['sections'][0]['rows'][0]['name']        
        # if there are no matches, return an empty dataframe
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
metadata_df.to_csv('../data/interim/rf_meta.csv', index=False)

####

# Debugging stuff

# Histogram of home values
# metadata_df.hist(column='home_value', bins=100)

# Get the index of a given address (useful for debugging)
# unique_addresses.index('816 S MAPLE AVE APT 2S')

# idx = range(2867, len(unique_addresses))  # subset of addresses - "debugging mode"



import pandas as pd
rf_metadata = pd.read_csv('../data/interim/rf_meta.csv')
rf_metadata['property_id'] = rf_metadata['property_id'].fillna(-1).astype(int)
rf_metadata


url=rf_metadata['search_url'][i]
pid=rf_metadata['property_id'][i]

# Function to get metadata from redfin
def get_year(url: str, pid: int):
    import requests
    import json
    import re
    from redfin import Redfin
    client = Redfin()
    page = requests.get('https://www.redfin.com/stingray/api/home/details/mainHouseInfoPanelInfo?propertyId=' + str(pid) + '&accessLevel=3&path=' + url, headers={'user-agent': 'redfin'})
    info = json.loads(page.text[4:])
    content = info['payload']['mainHouseInfo']['selectedAmenities'][1]['content']
    home_type = info['payload']['mainHouseInfo']['selectedAmenities'][3]['content']
    year_built = re.findall('Built in (\\d+)', content)[0]
    lot_size = re.findall('([0-9,]+)', info['payload']['mainHouseInfo']['selectedAmenities'][2]['content'])
    lot_size = float(lot_size[0].replace(',', ''))
    # Further data using redfin scraper
    result = client.page_tags(url)
    try:
        price = next((x for x in result['payload']['metaTags'] if x['name'] == 'twitter:text:price'), None)['content']
    except:
        price = float('nan')
    sqft = next((x for x in result['payload']['metaTags'] if x['name'] == 'twitter:text:sqft'), None)['content']
    beds = next((x for x in result['payload']['metaTags'] if x['name'] == 'twitter:text:beds'), None)['content']
    baths = next((x for x in result['payload']['metaTags'] if x['name'] == 'twitter:text:baths'), None)['content']

    return home_type, year_built, lot_size, price, beds, baths, sqft

# Testing zone
url='/IL/Oak-Park/1019-Highland-Ave-60304/home/13251221'
pid=13251221
# page = requests.get('https://www.redfin.com/stingray/api/home/details/mainHouseInfoPanelInfo?propertyId=' + str(pid) + '&accessLevel=3&path=' + url, headers={'user-agent': 'redfin'})
# info = json.loads(page.text[4:])
get_year(url, pid)



# Add home type and year built to the existing dataframe:
from tqdm.notebook import tqdm
from time import sleep

for i in tqdm(range(len(rf_metadata))):
    try:
        subdat = get_year(rf_metadata['search_url'][i], rf_metadata['property_id'][i])
        rf_metadata.loc[i, ['home_type', 'year_built', 'lot_size', 'price', 'beds', 'baths', 'sqft']] = subdat
    except:
        pass

# Save intermediate file
rf_metadata.head(50)
rf_metadata.columns

# Convert price to numeric
rf_metadata['price'] = rf_metadata['price'].str.replace('$', '').str.replace(',', '').astype(float)

# Convert beds to integer
rf_metadata['beds'] = rf_metadata['beds'].str.replace('BR', '').astype(float)

# Convert baths to numeric
rf_metadata['baths'] = rf_metadata['baths'].str.replace('BA', '').astype(float)

# Convert sqft to numeric
rf_metadata.loc[rf_metadata['sqft'] == '-', 'sqft'] = float('nan')
rf_metadata['sqft'] = rf_metadata['sqft'].str.replace(',', '').astype(float)

rf_metadata.reset_index(drop=True, inplace=True)

rf_metadata.to_csv('../data/interim/rf_meta_year_updated.csv', index=False)

