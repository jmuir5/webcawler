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
import types_1

"""
def getInfo(suffix, array, progress):
    result = ""
    line=""#
    while(result==""):
        try:
            result = requests.get(baseUrl+suffix.rstrip())
        except:
            print("thread "+progress+" encountered an error, trying again in 10 seconds")
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
"""

def getProduct(link, array, progress):
    product = fetch_product("", link.split("productdetails/")[1].split('/')[0],progress)

    title = product.split('"name":"')[1].split('",')[0]
    price = product.split('"price":')[2].split(',')[0]
    image = product.split('"image":"')[1].split('",')[0]
    sku = product.split('"sku":"')[1].split('",')[0]

    print("added #"+str(progress)+" successfully: "+title)

    array+=[title+", "+price+", "+image+", "+sku]
     

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

def fetch_product(cls, product_id: str, progress):
        url = f'https://www.woolworths.com.au/api/v3/ui/schemaorg/product/{product_id}'
        response=""
        attempts=0
        while(response==""):
            try:
                response = _session.get(url=url)
            except Exception as e:
                if(str(e).startswith("401 Client Error")):
                    print("thread "+str(progress)+" failed with 401 error. aborting") 
                    return '"name":"failed:'+product_id+'","price":0,"price":0,"image":"404","sku":"404"'
                print("thread "+str(progress)+" encountered an error: "+str(e)+", trying again in 10 seconds")
                sleep(10)
                attempts+=1
            else:
                break
            finally:
                if(attempts==10):
                   print("thread "+str(progress)+" failed 10 times. aborting thread") 
                   return '"name":"failed","price":0,"price":0,"image":"404","sku":"404"'
        
        return response.text



if __name__ == "__main__":

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
    #title, price, price per???, image, sku

    #product = fetch_product("", "129651")
    #title = product.split('"name":"')[1].split('",')[0]
    #price = product.split('"price":')[2].split(',')[0]
    #image = product.split('"image":"')[1].split('",')[0]
    #sku = product.split('"sku":"')[1].split('",')[0]
    #print(title+", "+price+", "+image+", "+sku)
    
    f=open("woolworthsLinks.txt", "r")
    o=open("woolworthsProducts.txt","w")
    productListings=[]
    progress=0
    threads = []

    for line in f:
        if(progress==1000):break
        progress+=1

        #getProduct(line, productListings)
        
        if (len(threads)%100==0):
            for thread in threads:
                thread.join()
        print("started thread #"+str(progress)+": "+line)
        T = threading.Thread(target=getProduct, args=(line, productListings, progress))
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
    
