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

def getProduct(link, array, progress,completed):
    product = fetch_product("", link.split("productdetails/")[1].split('/')[0],progress,completed)

    title = product.split('"name":"')[1].split('",')[0]
    price = product.split('"price":')[2].split(',')[0]
    image = product.split('"image":"')[1].split('",')[0]

    print("added #"+str(progress)+" successfully: "+title)

    array+=[title+", "+price+", "+image]
     

class DefaultTimeoutAdapter(HTTPAdapter):
    def __init__(self, *args, timeout: float, **kwargs):
        self.timeout = timeout
        super().__init__(*args, **kwargs)

    def send(self, request: PreparedRequest, **kwargs) -> Response:
        kwargs['timeout'] = kwargs.get('timeout') or self.timeout
        return super().send(request, **kwargs)


def new_session() -> requests.Session:
    """ Return requests.Session with batteries included; i.e. timeout, retries, error-raising. """
    session = requests_cache.CachedSession(backend='memory')
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    session.mount('https://', DefaultTimeoutAdapter(timeout=5, max_retries=retry_strategy))
    session.hooks = {
        'response': lambda r, *args, **kwargs: r.raise_for_status()
    }
    session.headers.update({
        'User-Agent': 'coles_vs_woolies'  # some User-Agent
    })
    return session

def _woolies_session():
    session = new_session()
    session.get(url='https://www.woolworths.com.au')
    return session

def fetch_product(cls, product_id: str, progress,completed):
        url = f'https://www.woolworths.com.au/api/v3/ui/schemaorg/product/{product_id}'
        response=""
        attempts=0
        while(response==""):
            try:
                response = _session.get(url=url)
                completed +=1
            except Exception as e:
                if(str(e).startswith("401 Client Error")):
                    print("thread "+str(progress)+" failed with 401 error. aborting") 
                    return '"name":"failed:'+product_id+'","price":0,"price":0,"image":"404"'
                print("thread "+str(progress)+" encountered an error: "+str(e)+", trying again in 1 minuite")
                sleep(60)
                attempts+=1
            else:
                break
            finally:
                if(attempts==10):
                   print("thread "+str(progress)+" failed 10 times. aborting thread") 
                   return '"name":"failed","price":0,"price":0,"image":"404"'
        
        return response.text



if __name__ == "__main__":
    start = time.time()
    numThreads=20
    #_session = _woolies_session()
    attempts = 0
    while(True):
        try:
            _session = _woolies_session()
        except:
            print("session generation encountered an error, trying again in 10 seconds")
            attempts+=1
            sleep(10)
        else:
            break
        finally:
            if(attempts == 10):
                print("session failed 10 times, aborting")
                exit()

    f=open("woolworthsLinks.txt", "r")
    o=open("woolworthsProducts.txt","w")
    productListings=[]
    progress=0
    completed=0
    threads = []

    for line in f:
        #if(progress==1000):break
        progress+=1

        #getProduct(line, productListings)
        
        if (len(threads)%numThreads==0):
            sleep(1)
            #for thread in threads:
             #   thread.join()
        print("started thread #"+str(progress)+": "+line)
        T = threading.Thread(target=getProduct, args=(line, productListings, progress,completed))
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
    end=time.time()
    totalTime=end-start
    print("process finished using "+str(numThreads)+" threads.\ntime taken: "+str(totalTime)+"\nsuccessfull entries: "+str(completed)+"/1000")

    #print(image)

"""process finished using100threads.
time taken: 345.606422662735
successfull entries: 9914/1000, 71 timeout, 86 failed"""

"""process finished using 10 threads.
time taken: 224.917982339859
successfull entries: 9985/1000, 0 timeout, 15 failed"""

"""process finished using 50 threads. bad run?
time taken: 660.2435896396637
successfull entries: 788/1000, 197 timeout, 212 failed"""
    
"""process finished using 50 threads.
time taken: 666.2105619907379
successfull entries: 0/1000"""

"""process finished using 20 threads.
time taken: 60.5791699886322
successfull entries: 0/1000 0 timeout"""

"""process finished using 30 threads.
time taken: 267.95836901664734
successfull entries: 0/1000 4 timeout"""

"""full job 20 threads old mode, 1592 failed, 961 timeout, 631 unauthorised (nicotine)"""

"""change timing to 1 second wait each 10 entries, wait for 1 minuite before retrying
0 TIMEOUT! 1/10 of the time!"""