from time import sleep
from bs4 import BeautifulSoup
import re
import requests
import threading


baseUrl = "https://www.coles.com.au"
suffix = "/product/bulla-ice-cream-choc-bars-vanilla-8pack-600ml-6277754"
result = requests.get(baseUrl+suffix.strip())

productPage = BeautifulSoup(result.text, 'html.parser')

print(productPage)
print(productPage.find("h1"))
print(productPage.find("h1").contents)
print(productPage.find("h1").contents[0])

