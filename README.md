# webcawler
this repository contains 4 webcrawlers used for the grocery CompariList (https://github.com/jmuir5/Grocery-CompariList). 
each webcrawler is split into 2 parts, the first scrapes the respective index.xml files for product pages, then the second scrapes the product pages for information. 
the webcrawlers make use of beautifulsoup and api(?) endpoints to collect information from the Coles, Woolworths, Iga and Aldi websites.
every webcrawler makes use of parelisation to improve efficancy in data scraping. 

i wanted to make a python script that would run all 4 crawlers then upload the file to firebase, but due the the problems encountered during the development of the CompariList, i never bothered to follow through on this front. 
