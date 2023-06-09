from bs4 import BeautifulSoup
import re
import requests

siteMaps = ["https://cdn0.woolworths.media/sitemap/sitemap1.xml", "https://cdn0.woolworths.media/sitemap/sitemap2.xml"]

f = open("woolworthsLinks.txt", "w")

links = []

for map in siteMaps:
    result = requests.get(map)#+browse+categories[0])
    soup3 = BeautifulSoup(result.text, 'xml')
    for link in soup3.find_all(string = re.compile("/productdetails/")):
          if(links.count(link)<=0):
              links+=[link]

for line in links:
    f.write(str(line)+"\n")
f.close()
print("woolworths crawling finished successfully, "+str(len(links))+" links saved to 'woolworthsLinks.txt'")