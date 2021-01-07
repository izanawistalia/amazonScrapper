import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def get_url(search_term):
    url = 'https://www.amazon.com/s?k={}&qid=1609774652&ref=sr_pg_1'
    search_term=search_term.replace(' ','+')
    url = url.format(search_term)
    return url

def extract_info(item):
    item_name = item.h2.text.strip()
    try:
        item_rating = item.find('span',class_='a-icon-alt').text
    except AttributeError:
        item_rating = 'NONE'
    try:
        item_reviews = item.find('span',{'class':'a-size-base','dir':'auto'}).text
    except AttributeError:
        item_reviews = 'NONE'
    try:
        item_price = item.find('span',class_='a-offscreen').text
    except AttributeError:
        return

    print(f'{item_name} has a rating of {item_rating} and {item_reviews} reviews, and has the price of {item_price}.')
    
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(get_url('mobile phone'))
for page in range(1,21):
    soup = BeautifulSoup(driver.page_source,'lxml')
    items = soup.find_all('div',{'data-component-type':'s-search-result'})

    for item in items:
        extract_info(item)
        print()
        print('-------------------------------------------------------------------------------------------------------------------------------------')
        print()
    url = 'https://amazon.com'+soup.find('li',class_='a-last').a['href']
    driver.get(url)