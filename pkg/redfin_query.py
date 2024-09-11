# I got this code elsewhere
def search_houses(self='https://www.redfin.com/city/60304/IL/Oak-Park/', query):
    """
    Given the query string (i.e. sold-6mo), we search the houses from Redfin.
    Arguments:
        query {str} -- a query string that acts as the filter of the search
    """

    url = self.url + \
        '/filter/include={}'.format(query)
    return url

    # soup = self.get_page_soup(url)

    # # first finds the number of pages in the search list
    # numPages = int(soup.find_all('span', attrs={'class': 'pageText'})[
    #     0].text.split()[-1])
    # # loop through every page of the search result
    # for i in range(numPages):
    #     # if this is not the first iteration, go to the next page of the search results
    #     if i != 0:
    #         soup = self.get_page_soup(url + '/page-{}'.format(i+1))
    #         self.random_sleep()
    #     # get the corresponding information on the page
    #     try:
    #         ids = list(map(lambda tag: tag['href'].split('/')
    #                         [-1], soup.find_all('a', attrs={'class': 'cover-all'})))
    #         addresses = list(map(lambda tag: tag.text, soup.find_all(
    #             'span', attrs={'data-rf-test-id': 'abp-streetLine'})))
    #         statusDates = list(map(lambda tag: self.parse_status_dates(tag.text), soup.find_all(
    #             'span', attrs={'class': 'HomeSash font-weight-bold roundedCorners'})))
    #         prices = list(map(lambda tag: tag.text, soup.find_all(
    #             'span', attrs={'class': 'homecardV2Price'})))
    #         stats = [list(map(lambda tag: tag.text, singleHouseStats))
    #                     for singleHouseStats in soup.find_all('div', attrs={'class': 'HomeStatsV2'})]
    #         print("Finished page {}/{} of the results".format(i+1, numPages))
    #     except:
    #         raise("Exception occurred when parsing the information from the page {}.The page might have been changed and the scraping script is probably not updated.".format(url))

    #     # loop through all information we obtained and store them as house objects
    #     for j in range(len(ids)):
    #         id = ids[j]
    #         if (j < len(addresses)):
    #             address = addresses[j]
    #         if (j < len(statusDates)):
    #             [status, date] = statusDates[j]
    #         if (j < len(prices)):
    #             price = prices[j]
    #         if (j < len(stats)):
    #             [bed, bath, size] = stats[j]
    #         # self.houses[id] = (House(id=id, streetAddress=address, status=status, date=date,
    #         #                          lastListedPrice=price, numBed=bed, numBath=bath, size=size))
    #         #
    #         # alternatively keep a dataframe
    #         self.houses = self.houses.append(
    #             {'id': id, 'address': address, 'status': status, 'date': date, 'lastListedPrice': price, 'numBed': bed, 'numBath': bath, 'size': size}, ignore_index=True)
