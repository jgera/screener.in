import urllib.request
from retry import retry
import logging

logging.basicConfig(filename='log.txt', filemode='a',format='%(asctime)s - %(message)s', level=logging.INFO)

## Todo
# https://www.scrapehero.com/how-to-fake-and-rotate-user-agents-using-python-3/

def urlread(url,**kwargs):

    if "header" in kwargs:
        hdr = kwargs["header"]
    else:
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive',
          }

    req = urllib.request.Request(url,None,hdr)
    response = urllib.request.urlopen(req)   
    data = response.read()
    return data.decode('utf-8')


@retry(urllib.request.URLError, tries=1, delay=3, backoff=2)
def urlretry1(url):
   return urlread(url)

@retry(urllib.request.URLError, tries=3, delay=3, backoff=2)
def urlretry(url):
   return urlread(url)

@retry(urllib.request.URLError, tries=2, delay=3, backoff=2)
def urlretry3(url):
   return urlread(url)

@retry(urllib.request.URLError, tries=5, delay=3, backoff=2)
def urlretry5(url):
   return urlread(url)

@retry(urllib.request.URLError, tries=1, delay=3, backoff=2)
def urlretry3log(url):
   d = None
   try:
      d = urlread(url)
   except:
      print('urlread failed:' + url)
      logging.info(url)
   return d

@retry(urllib.request.URLError, tries=5, delay=3, backoff=2)
def urlretry5log(url):
   d = None
   try:
      d = urlread(url)
   except:
      print('urlread failed:' + url)
      logging.info(url)
   return d



