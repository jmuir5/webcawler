from time import sleep
from bs4 import BeautifulSoup
import re
import requests
import threading


def getInfo(line, array, progress):
    result = ""
    while(result==""):
        try:
            result = requests.get(line)
        except:
            print("thread "+str(progress)+" encountered an error, trying again in 10 seconds")
            sleep(10)

    productPage = BeautifulSoup(result.text, 'html.parser')

    try:
        title=""
        for element in productPage.find("h1"):
            try:
                title+=element.strip()
            except:
                title+=element.contents[0].strip()
    except Exception as e:
        array+=[""+line+", $0.00, xxx, 404"]
        print("failed to add #"+str(progress)+": "+line+" "+str(e))
        return
    try:
        price = productPage.find(attrs={"class": "box--value"}).contents[0]+productPage.find(attrs={"class": "box--decimal"}).contents[0]
    except:
        price = "currently unavailable"
    try:
        pricingMethod = productPage.find(attrs={"class": "detail-box--price-box--price--detailamount box--detailamount"}).contents[0]
    except:
        pricingMethod = price+" per each"
    try:
        image = productPage.find_all("img")[0].get('src')
    except:
        image = "404"

    array+=[""+title+", "+price+", "+pricingMethod+", "+image+""]
    print("added #"+str(progress)+" successfully: "+title)



if __name__ == "__main__":
    f=open("aldiLinks.txt", "r")
    o=open("aldiProducts.txt","w")
    productListings=[]
    progress=0
    threads = []

    for line in f:
        if (len(threads)%100==0):
            for thread in threads:
                thread.join()
        progress+=1
        print("started thread #"+str(progress)+": "+line)
        T = threading.Thread(target=getInfo, args=(line.strip(), productListings, progress))
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
