# Automatically download photos from historic homes website
# https://dghistory.org/american-foursquares/

from bs4 import BeautifulSoup
import requests
import os

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0)   Gecko/20100101 Firefox/78.0", 
"Referer": "https://www.google.com"}

# this is where the links to the pages with images are
def get_image_page_links(soup):
    images = soup.find_all(class_='elementor-post__thumbnail__link')    
    links = [x.get('href') for x in images]
    # only keep links if they have the word house or home in them
    links = [x for x in links if 'house' in x or 'home' in x]
    return links

# save image to disk
def save_image(image_url, folder='images'):
    if not os.path.exists(folder):
        os.makedirs(folder)
    image_name = os.path.join(folder, image_url.split('/')[-1])
    img_data = requests.get(image_url, headers=headers).content
    with open(image_name, 'wb') as f:
        f.write(img_data)

# get image links within a page
def get_image_link(url, download=False, folder='images'):
    page = requests.get(url, headers=headers)
    page_soup = BeautifulSoup(page.content, 'html.parser')
    images = page_soup.find_all('img')
    image_urls = [img.get('src') for img in images]
    if download:
        save_image(image_urls[2], folder=folder)
    return image_urls[2] # only return the third image - looking at page structure this is where the biggest photo is

# Download a single image
# save_image(image_urls[2], folder='images/queen_anne/test')


# Search for a specific house type
type='foursquare'
def search_for_house_type(type, path='images'):
    url = 'https://dghistory.org/?s=' + type
    html_page = requests.get(url, headers=headers)
    soup = BeautifulSoup(html_page.content, 'html.parser')
    # Get the number of pages
    pages = soup.find_all(class_='page-numbers')
    # Text type
    type = type.replace('+', '_')
    # Download linked images from the first page
    links = get_image_page_links(soup)
    for link in links:
        get_image_link(link, download=True, folder=path)
    # Download linked images from the rest of the pages
    if len(pages) > 1:
        for p in range(1, len(pages)-1):
            html_page = requests.get(pages[p]['href'], headers=headers)
            soup = BeautifulSoup(html_page.content, 'html.parser')
            links = get_image_page_links(soup)
            for link in links:
                get_image_link(link, download=True, folder=path)

# Now do the searching...
search_for_house_type('prairie', path='images/training/prairie')
search_for_house_type('bungalow', path='images/training/bungalow')
search_for_house_type('foursquare', path='images/training/foursquare')
search_for_house_type('queen+anne', path='images/training/victorian')

# TODO figure out why it's always downloading the image '4703-Highland-Ave...jpg'
