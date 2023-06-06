from bs4 import BeautifulSoup
import re
import requests

url = "https://www.coles.com.au"
result = requests.get(url+"/browse")
colesCategories = BeautifulSoup(result.text, 'html.parser')

f = open("colesLinks.txt", "w")

links = []
categoryList = []
for category in colesCategories.find_all(href = re.compile("/browse/")):
    categoryList+=[category.get('href')]
    

for suffix in categoryList:
    print("started "+suffix+", current len = "+str(len(links)))
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
    

#print(links)
for line in links:
    f.write(str(line)+"\n")
f.close()
print("coles crawling finished successfully, "+str(len(links))+" links saved to 'colesLinks.txt'")