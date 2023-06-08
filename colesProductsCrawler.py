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
    except:
        array+=[""+line+", $0.00", "xxx", "404"]
        print("failed to add #"+str(progress)+": "+line)
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

    array+=[""+title+", "+price+", "+pricingMethod+", "+image+""]
    print("added #"+str(progress)+" successfully: "+title)



if __name__ == "__main__":
    baseUrl = "https://www.coles.com.au"
    f=open("colesLinks.txt", "r")
    o=open("colesProducts.txt","w")
    productListings=[]
    progress=0
    threads = []

    for line in f:
        if (len(threads)%100==0):
            for thread in threads:
                thread.join()
        progress+=1
        print("started thread #"+str(progress)+": "+line)
        T = threading.Thread(target=getInfo, args=(line, productListings, progress))
        threads.append(T)
        T.start()    

    for thread in threads:
        thread.join()

    print("all threads completed, writing to file")

    for line in productListings:
        o.write(str(line)+"\n")
    f.close()
    o.close()
    print("job done")

    #print(image)
