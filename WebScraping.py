import requests
from bs4 import BeautifulSoup

url = "https://webscraper.io/test-sites/e-commerce/allinone/phones/touch"
page = requests.get(url)

soup = BeautifulSoup(page.text, 'lxml')


print(soup.text)
"""first_item = soup.find("div", {"class": "col-sm-4 col-lg-4 col-md-4"} )
prices = soup.find_all("h4", {"class": "price float-end card-title pull-right"} )
items = soup.find_all("a", {"class": "title"})
print(prices)
catalog = {}
for item,price in zip(items,prices):
    
    catalog[item.text] = float(str(price.text)[1:])


print(catalog)
print("Average price: ", round(sum(catalog.values())/len(catalog),2))
"""
"""item_count = len(prices)
total = 0
for tag in prices:
    price = float(str(tag.text)[1:])
    total += price


print(round(total/item_count,2))"""

