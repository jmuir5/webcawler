from bs4 import BeautifulSoup
import re
import requests
import threading

def getColesLinks(suffix, array):
    url = "https://www.coles.com.au"
    print("started "+suffix+", current len = "+str(len(array)))
    result = requests.get(url+suffix)
    soup3 = BeautifulSoup(result.text, 'html.parser')
    page=1
    while(True):
      print("page "+str(page)+" of "+suffix)
      for link in soup3.find_all(href = re.compile("/product/")):
          if(array.count(link.get('href'))<=0):
              array+=[link.get('href')]
      if(soup3.find(id="pagination-button-next")):
          page+=1
          result = requests.get(url+suffix+"?page="+str(page))
          soup3 = BeautifulSoup(result.text, 'html.parser')
      else:
          print("finished "+suffix+", current len = "+str(len(links)))
          break

url = "https://www.coles.com.au"
result = requests.get(url+"/browse")
colesCategories = BeautifulSoup(result.text, 'html.parser')

f = open("colesLinks.txt", "w")

links = []
threads = []
categoryList = []
for category in colesCategories.find_all(href = re.compile("/browse/")):
    categoryList+=[category.get('href')]
    

for suffix in categoryList:
    T = threading.Thread(target=getColesLinks, args=(suffix, links))
    threads.append(T)
    T.start() 
for thread in threads:
        thread.join()

"""print("started "+suffix+", current len = "+str(len(links)))
    result = requests.get(url+suffix)
    soup3 = BeautifulSoup(result.text, 'html.parser')
    page=1
    while(True):
      print("page "+str(page)+" of "+suffix)
      for link in soup3.find_all(href = re.compile("/product/")):
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
print("coles crawling finished successfully, "+str(len(links))+" links saved to 'colesLinks.txt'")