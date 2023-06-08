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

result = requests.get("https://www.igashop.com.au/api/storefront/stores/52511/products/22183")
soup3 = BeautifulSoup(result.text, 'html.parser')
print(soup3)