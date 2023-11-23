import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# Function to extract Product Title
def get_title(soup):

    try:
        # Outer Tag Object
        title = soup.find("h1", class_="name")

        # Title as a string value
        title_string = title.text.strip()

    except AttributeError:
        title_string = ""

    return title_string

# Function to extract Product Price
def get_price(soup):

    try:
        price = soup.find("p", class_="price").text.strip()

    except AttributeError:
            price = "CHECK PRICE IN CART"

    return price

if __name__ == '__main__':
     
    # Define URL
    URL  = 'https://ohiostate.bncollege.com/Categories/Supplies--Technology/Computer--Electronics/c/ac-supplies-computer-electronics?pageSize=90&q=%3AtopRated%3ASale%3Atrue#'

    # Headers for request
    HEADERS = ({'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36': '', 'Accept-Language': 'en-US, en; q = 0.5'})

    # Send HPPT Request
    resp = requests.get(URL , HEADERS)

    # Soup object containing all data(changing from byte format of webpage to html format)
    soup = BeautifulSoup(resp.content, "html.parser")

    # Fetch links as list of Tag objects using inspect element
    links = soup.find_all('a', class_= "name js-dotdotdot")

    # Storage for the corrected links
    links_list = []

    # Loop for extracting product details from Tag objects
    for link in links:
         links_list.append(link.get('href'))

    
    d = {"Title":[], "Price":[]}


    # Loop for extracting product details from each link    
    for link in links_list:
        new_webpage = requests.get('https://ohiostate.bncollege.com' + link, HEADERS)

        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        # Function calls to display all necessary product information
        d['Title'].append(get_title(new_soup))
        d['Price'].append(get_price(new_soup))
        

    BN_df = pd.DataFrame.from_dict(d)
    BN_df['Title'].replace('', np.nan, inplace=True)
    BN_df = BN_df.dropna(subset =['Title'])
    BN_df.to_csv("BNSales_data.csv", header = False, index = False)

    with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 2,
                       ):

        print(BN_df)