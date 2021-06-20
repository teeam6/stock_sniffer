import os, sys, json, requests, hashlib, csv, pendulum
from lib.utils import Utils
from pydantic import BaseModel
from model import Stock
from bs4 import BeautifulSoup

class WebParser:
    def __init__(self):
        self.utils = Utils()
        self.cfg = self.utils.cfg
        self.stocks = self.cfg['stocks'].split(',')
        self.url = self.cfg['url']
        self.start_workflow()

    def start_workflow(self):
        for s in self.stocks:
            price = self.get_stock_price(s)
            dic = {
                'short': s,
                'price': price,
                'timestamp': self.get_time(),
                'url': self.url + s
            }
            print(Stock(**dic))
        
    
    @staticmethod
    def get_time():
        dt = pendulum.now()
        return dt.format('DD-MM-YYYYTHH:mm:ss')

    '''
        name: get_stock_price
        args: s - stock short name
        desc: get web page content from link in config parametr 'url'
              and parse it by tags 'h3' > 'bg-quote'
    '''
    def get_stock_price(self, s):
        url = self.url+s
        try:
            self.utils._debug("Trying to get web page")
            response = requests.get(url)
        except Exception as e:
            self.utils._error("Cannot get web page: "+str(e))
            sys.exit(1)

        soup = BeautifulSoup(response.content, 'html.parser')
        result = soup.find_all('h3', class_='intraday__price')
        for i in result:
            price = i.find('bg-quote', class_='value')
            self.utils._debug("Price for {}: {}".format(s.upper(), price.text))
        if price:
            return float(price.text.replace(',', ''))
        else:
            self.utils._error("Cannot obtain price from web page")
            return None


if __name__ == '__main__':
    WebParser()
    