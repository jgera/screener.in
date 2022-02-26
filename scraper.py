import json
from symtable import Symbol
from urlread import *
import logging
import csv
import requests
import os
import re
from time import sleep


logging.basicConfig(filename='log.txt', filemode='a',format='%(asctime)s - %(message)s', level=logging.DEBUG)
console = logging.StreamHandler()
logging.getLogger().addHandler(console)

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "en-US,en;q=0.9,hi;q=0.8",
    "cache-control": "max-age=0",
    "content-type": "application/x-www-form-urlencoded",
    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"98\", \"Google Chrome\";v=\"98\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "cookie": "csrftoken=I7FasdasdsamHZfqY4duaGsB0jgi1BQFlNmifDmbd sessionid=sdsdadsdsds; _gcl_au=1.1.602809564.1645862651; _ga=GA1.2.",
    "Referer": "https://www.screener.in/company/TATAMOTORS/consolidated/",
    "Referrer-Policy": "no-referrer-when-downgrade"
  }

postdata = "csrfmiddlewaretoken=FWEEawGRsB2XkdKTSMxkRao1OZzlv2xq&next=%2Fcompany%2FTATAMOTORS%2Fconsolidated%2F"


def getReport(warehouseid,symbol,PATH):
    url = 'https://www.screener.in/user/company/export/{}/'.format(warehouseid)
    r = requests.post(url, data= postdata, headers=headers)
    path = '{}/{}.xlsx'.format(PATH,symbol.strip())
    
    # Export to xlsx
    if r.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in r:
                f.write(chunk)

def Scrape(symbols,PATH,delay=0):
    data = []
    rexp = 'formaction=.\/user\/company\/export/([0-9]+)\/.'
    for symbol in symbols:
        api = "https://www.screener.in/api/company/search/?q=" + symbol    
        logging.info("Getting: " + api)
        try:
            d = urlread(api)
            j = json.loads(d)[0]
            html = urlread('https://www.screener.in' + j['url'])        
            results = re.findall(rexp,html)
            print("Warehouse Id = " + results[0])      
            
            j['warehouse'] = results[0]
            data.append(j)        
            logging.info("Downloading: " + symbol)
            getReport(results[0],symbol,PATH)
        except:
            print("Error: " + api)
            logging.ERROR(api)
        sleep(delay)
    ExportLinks(data)

def ExportLinks(data):   
    with open("links.csv","w",newline="") as f:  
        title = "id,name,url,warehouse".split(",")
        cw = csv.DictWriter(f,title,delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        cw.writeheader()
        cw.writerows(data)

print("Finished.")


import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scraper for www.screener.in')
    parser.add_argument('-s','--symbols', help='comma Seperated Symbols or a File constaining Sybols to scrape', required=False, default="TCS,INFY,WIPRO")
    parser.add_argument('-p','--path', help='directory to store reports default reports/', required=False, default='.')
    parser.add_argument('-l','--log', help='log file default log.txt', required=False, default='log.txt')
    parser.add_argument('-d','--delay', help='delay in downloading to avoid HTTP error 429 (Too Many Requests)', required=False, default=60)
    parser.add_argument('-e','--export', help='export links to csv', required=False, default=False)        
    args = parser.parse_args()
      
    if not os.path.exists(args.symbols):
        symbols = args.symbols.split(",")
    else:
        symbols = open(args.symbols,'r').readlines()

    # create reports folder if not exists
    PATH = args.path
    if not os.path.exists(args.path):
        os.makedirs(args.path)

    Scrape(symbols,PATH,args.delay)
    