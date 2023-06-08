from bs4 import BeautifulSoup
import re
import requests

siteMap = "https://www.igashop.com.au/product-sitemap.xml"

f = open("igaLinks.txt", "w")

links = []

result = requests.get(siteMap)
soup3 = BeautifulSoup(result.text, 'xml')
for link in soup3.find_all(string = re.compile("/product/")):
        if(links.count(link)<=0):
            links+=[link]

for line in links:
    f.write(str(line)+"\n")
f.close()
print("iga crawling finished successfully, "+str(len(links))+" links saved to 'igaLinks.txt'")