# 

import requests

from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0)   Gecko/20100101 Firefox/78.0", 
"Referer": "https://www.google.com"}

url = "https://www.redfin.com/zipcode/60304/filter/property-type=house,include=sold-5yr"
# this should get us 981 homes

resp = requests.get(url, headers=headers, verify=False)


neighborhoods = ""



"https://www.cookcountyassessor.com/ajax/clarity_pin_search/next?provider=neighborhood&town=Oak+Park&town_id=27&neighborhoodCode=100&classification=none&pages=43&page=25&_wrapper_format=drupal_ajax"
