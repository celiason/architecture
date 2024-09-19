# TODO come up with a better name for this package ('pkg' is not very descriptive)

# create a label function
def label_func(f):
    import re
    return f[0].isupper()

# I think this function is showing a batch of images
# def _batch_ex(bs):
#     from fastai.vision.all import TensorImage
#     return TensorImage(timg[None].expand(bs, *timg.shape).clone())

# function to get an image from a redfin listing
def get_redfin_image(address, clean=False):
    import urllib.request
    import os
    import re

    long_address = address + ", Oak Park"

    # sometimes the address has a direction in it, which messes up the search
    if clean:
        long_address = re.sub(r'\s[NSEW]\.*\s', ' ', long_address)
    
    response = client.search(long_address)
    url = response['payload']['exactMatch']['url']
    
    # get info
    initial_info = client.initial_info(url)
    img = initial_info['payload']['preloadImageUrls']
    
    # format the address
    address = address.replace(' ', '-')
    
    # extract IDs for later
    pid = str(initial_info['payload']['propertyId'])
    lid = str(initial_info['payload']['listingId'])
    
    # Download the image from the URL and save it as a file
    image_url = img[0]
    file_name = "images/testing/" + address + "_pid" + pid + "_lid" + lid + ".jpg"
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    
    urllib.request.urlretrieve(image_url, file_name)
