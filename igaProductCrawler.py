import time
from time import sleep
from bs4 import BeautifulSoup
import re
import requests
import requests_cache
import threading
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter, Retry
from requests import PreparedRequest, Response
from typing import Any, Generator, Optional
from pydantic import BaseModel, Extra

def getProduct(product_id, array, progress):
    url = f'https://www.igashop.com.au/api/storefront/stores/52511/products/{product_id}'
    response=""
    attempts=0
    while(response==""):
        try:
            response = requests.get(url).text
        except Exception as e:
            if(str(e).startswith("401 Client Error")):
                print("thread "+str(progress)+" failed with 401 error. aborting") 
                response = '"name":"failed:'+product_id+'","price":0,"price":0,"image":"404","sku":"404"'
            print("thread "+str(progress)+" encountered an error: "+str(e)+", trying again in 1 minuite")
            sleep(60)
            attempts+=1
        else:
            break
        finally:
            if(attempts==10):
                print("thread "+str(progress)+" failed 10 times. aborting thread") 
                response = '"name":"failed","price":0,"price":0,"image":"404","sku":"404"'
    try:   
        title = response.split('"name":"')[1].split('",')[0]
        price = response.split('"price":')[1].split(',')[0]
        unitprice = response.split('"unitPrice":')[1].split(',')[0]
        image = response.split('"default":"')[1].split('",')[0]
        sku = response.split('"sku":"')[1].split('",')[0]
        print("added #"+str(progress)+" successfully: "+title)
        array+=[title+";"+price+";"+unitprice+";"+image+";"+sku]
    except Exception as e:
        errorCode = response.split('"statusCode":')[1].split(',')[0]
        sleep(10)
        print("failed to add #"+str(progress)+": "+errorCode)

    

    
     


if __name__ == "__main__":
    start = time.time()
    #numThreads=1000
    f=open("igaLinks.txt", "r")
    
    productListings=[]
    progress=0
    threads = []

    for line in f:
        #if(progress==10):break
        progress+=1
        
        #if (len(threads)%numThreads==0):
            #sleep(1)
            #for thread in threads:
            #   thread.join()
        print("started thread #"+str(progress)+": "+line)
        T = threading.Thread(target=getProduct, args=(line.split("https://www.igashop.com.au/product/")[1].strip(), productListings, progress))
        threads.append(T)
        T.start()    

    for thread in threads:
        thread.join()
    
    print("all threads completed, writing to file")

    o=open("igaProducts.txt","w")
    for index, line in enumerate(productListings):
        
        o.write(str(line))
        if (index!=len(productListings)-1):
            o.write("\n")
    f.close()
    o.close()
    print("job done")
    end=time.time()
    totalTime=end-start
    print("process finished using unlimited threads.\ntime taken: "+str(totalTime))

