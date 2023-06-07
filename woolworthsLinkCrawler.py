from bs4 import BeautifulSoup
import re
import requests

siteMaps = ["https://cdn0.woolworths.media/sitemap/sitemap1.xml", "https://cdn0.woolworths.media/sitemap/sitemap2.xml"]
#browse = "/browse"
#categories = ["/fruit-veg","/bakery","/lunch-box","/poultry-meat-seafood","/deli-chilled-meals","/dairy-eggs-fridge","/pantry","/health-wellness","/snacks-confectionery","/beauty-personal-care","/freezer","/drinks","/baby","/pet","/cleaning-maintenance","/home-lifestyle"]

f = open("woolworthsLinks.txt", "w")

links = []

for map in siteMaps:
    result = requests.get(map)#+browse+categories[0])
    soup3 = BeautifulSoup(result.text, 'xml')
    for link in soup3.find_all(string = re.compile("/productdetails/")):
          if(links.count(link)<=0):
              links+=[link]
#result = requests.get(baseUrl)#+browse+categories[0])
#soup3 = BeautifulSoup(result.text, 'xml')
#print(soup3.find(string = re.compile("/productdetails/")))
#for link in soup3.find_all("shared-product-tile"):
 #         print(link.get('href'))
"""
for suffix in categories:
    print("started "+suffix+", current len = "+str(len(links)))
    result = requests.get(baseUrl+browse+suffix)
    soup3 = BeautifulSoup(result.text, 'html.parser')
    page=1
    while(True):
      print("page "+str(page)+" of "+suffix)
      for link in soup3.find_all("shared-product-tile"):
          if(links.count(link.get('href'))<=0):
              links+=[link.get('href')]
      if(soup3.find(id="pagination-button-next")):
          page+=1
          result = requests.get(url+suffix+"?page="+str(page))
          soup3 = BeautifulSoup(result.text, 'html.parser')
      else:
          print("finished "+suffix+", current len = "+str(len(links)))
          break
    """

#print(links)
for line in links:
    f.write(str(line)+"\n")
f.close()
print("woolworths crawling finished successfully, "+str(len(links))+" links saved to 'woolworthsLinks.txt'")