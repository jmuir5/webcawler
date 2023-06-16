from time import sleep
from bs4 import BeautifulSoup
import re
import requests
import threading


def getInfo(suffix, array, progress):
    result = ""
    while(result==""):
        try:
            result = requests.get(baseUrl+suffix.strip())
        except Exception as e:
            print("thread "+str(progress)+" encountered an error: "+str(e)+", trying again in 10 seconds")
            sleep(10)

    productPage = BeautifulSoup(result.text, 'html.parser')

    try:
        title = productPage.find("h1").contents[0]
    except Exception as e:
        #array+=[""+line+", $0.00", "xxx", "404"]
        print("failed to add #"+str(progress)+": "+line+", exception:"+str(e))
        return
    try:
        price = productPage.find(attrs={"data-testid": "pricing"}).contents[0]
    except:
        price = "currently unavailable"
    try:
        pricingMethod = productPage.find(attrs={"class": "price__calculation_method"}).contents[0]
    except:
        pricingMethod = price+" per each"
    try:
        image = productPage.find_all("img")[2].get('src')
    except:
        image = "404"
    try:
        sku = productPage.find(attrs={"data-testid": "product-code"}).contents[3]
    except:
        sku = "currently unavailable"

    array+=[""+title+","+price+","+pricingMethod+","+image+","+sku]
    print("added #"+str(progress)+" successfully: "+title)



if __name__ == "__main__":
    baseUrl = "https://www.coles.com.au"
    f=open("colesLinks.txt", "r")
    o=open("colesProducts.txt","w")
    productListings=[]
    progress=0
    threads = []

    for line in f:
        numThreads = 10
        if (len(threads)%numThreads==0):
            sleep(1)
        progress+=1
        print("started thread #"+str(progress)+": "+line)
        T = threading.Thread(target=getInfo, args=(line, productListings, progress))
        threads.append(T)
        T.start()    

    for thread in threads:
        thread.join()

    print("all threads completed, writing to file")

    for index, line in enumerate(productListings):
        
        o.write(str(line))
        if (index!=len(productListings)-1):
            o.write("\n")
    f.close()
    o.close()
    print("job done")

    #print(image)
