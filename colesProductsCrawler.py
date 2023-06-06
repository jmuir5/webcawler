from bs4 import BeautifulSoup
import re
import requests

baseUrl = "https://www.coles.com.au"
f=open("colesLinks.txt", "r")
o=open("colesProducts.txt","w")
productListings=[]
progress=0

for line in f:
    result = requests.get(baseUrl+line.rstrip())
    productPage = BeautifulSoup(result.text, 'html.parser')

    try:
        title = productPage.find("h1").contents[0]
    except:
        productListings+=[line, "$0.00", "xxx", "404"]
        print("failed to add #"+str(progress)+": "+line)
        continue
    try:
        price = productPage.find(attrs={"data-testid": "pricing"}).contents[0]
    except:
        price = "currently unavailable"
    try:
        pricingMethod = productPage.find(attrs={"class": "price__calculation_method"}).contents[0]
    except:
        pricingMethod = price+" per each"
        
    image = productPage.find_all("img")[2].get('src')
    productListings+=[title, price, pricingMethod, image]
    print("added #"+str(progress)+" successfully: "+title)
    progress+=1

for line in productListings:
    o.write(str(line)+"\n")
f.close()
o.close()

print(image)
