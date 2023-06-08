from bs4 import BeautifulSoup
import re
import requests
import threading

def getLinks(url, array):
    result = requests.get(url)
    soup3 = BeautifulSoup(result.text, 'xml')
    for link in soup3.find_all(string = re.compile("/ps/p/")):
          if(array.count(link)<=0):
              array+=[link]


baseUrl="https://www.aldi.com.au/en/groceries/"
categories =["super-savers","seasonal-range","price-reductions","fresh-produce","baby","beauty","freezer","health","laundry-household","liquor","pantry"]
sitemapSuffix = "/sitemap.xml"


links = []
threads = []

for category in categories:
    T = threading.Thread(target=getLinks, args=(baseUrl+category+sitemapSuffix, links))
    threads.append(T)
    T.start() 
for thread in threads:
        thread.join()

f = open("aldiLinks.txt", "w")
for line in links:
    f.write(str(line)+"\n")
f.close()
print("aldi crawling finished successfully, "+str(len(links))+" links saved to 'aldiLinks.txt'")