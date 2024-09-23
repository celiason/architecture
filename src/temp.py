# This is temp, can probably be removed


#### Try #1 ####################

# other data?
# look at how (selling?) price of homes is affected by the way it's described
# would be cool if I can do image analysis on homes to classify actual architectural style

main_url = "https://www.redfin.com/IL/Oak-Park/613-S-Grove-Ave-60304/home/13249167"

# Getting individual cities url
# re = requests.get(main_url)
# soup = BeautifulSoup(re.text, "html.parser")
# soup

# NB this failed because they think it's a bot

# let's try something else
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0)   Gecko/20100101 Firefox/78.0", 
"Referer": "https://www.google.com"}

main_url = "https://www.redfin.com/zipcode/60304"

response = requests.get(main_url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
# this works!
soup

# 

import requests

from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0)   Gecko/20100101 Firefox/78.0", 
"Referer": "https://www.google.com"}

url = "https://www.redfin.com/zipcode/60304/filter/property-type=house,include=sold-5yr"
# this should get us 981 homes

resp = requests.get(url, headers=headers, verify=False)

soup=BeautifulSoup(resp.text,'html.parser')
allBoxes = soup.find_all("div",{"class":"HomeCardContainer"})


#### Try #2 ####################

# functino to scrape
def scrape_redfin(address: str):
    # search based on text
    url = "redfin.com/IL/Oak-Park/" + address + 60304 + "/home/"
    resp = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(resp.text,'html.parser')
    #allBoxes = soup.find_all("div",{"class":"HomeCardContainer"})

    # try return
    return soup
    # get metadata

    # keep only if single-family home

# scrape_redfin(address = unique_addresses[0])

address = unique_addresses[1]


address = ' '.join(word.capitalize() for word in address.split())
address = address.replace(' ', '-')
address = address.replace('Av\b', 'Ave\b')

address

url = "www.redfin.com/IL/Oak-Park/" + address + "-60304/home/"
# resp = requests.get(url, headers=headers, verify=False)

url


#### Try #3 ####################

def search_houses(query):
    """
    Given the query string (i.e. sold-6mo), we search the houses from Redfin.
    Arguments:
        query {str} -- a query string that acts as the filter of the search
    """
    self='https://www.redfin.com/city/14204/IL/Oak-Park/'
    url = self + 'filter/include={}'.format(query)
    return url

# search_houses(query='613 S Grove Ave')
# url = "https://www.redfin.com/stingray/do/location-autocomplete?location=613%20S%20Grove%20Ave&start=0&count=10&v=2&market=chicago&al=1&iss=false&ooa=true&mrs=false&region_id=NaN&region_type=NaN&lat=41.8777742&lng=-87.7956339"


