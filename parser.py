import os, sys, json, requests, hashlib, csv, pendulum
from pathlib import Path
from lib.utils import Utils
from pydantic import BaseModel
from model import Stock, Crypto, Index, Future
from bs4 import BeautifulSoup

class WebParser:
    def __init__(self):
        self.utils = Utils()
        self.cfg = self.utils.cfg
        # self.stocks = self.cfg['stocks'].split(',')
        self.index_url = self.cfg['index_url'].split(',')
        self.crypto_url = self.cfg['crypto_url'].split(',')
        self.future_url = self.cfg['index_url'].split(',')
        self.indexes = self.cfg['indexes'].split(',')
        self.cryptos = self.cfg['cryptos'].split(',')
        self.futures = self.cfg['futures'].split(',')
        self.start_workflow()

    def start_workflow(self):
        if not self.time_check():
            self.utils._debug("there is not time yet...")
            sys.exit(1)

        index_arr = []
        for _i in self.indexes:
            url = self.index_url[0]+_i
            price = self.get_index_price(url)
            if price:
                dic = {
                    'name': _i.split('?')[0],
                    'price': price,
                    'timestamp': self.get_time(),
                    'url': url
                }
                index_arr.append(dic)
        url = self.index_url[1]
        price = self.get_index_price(url)
        if price:
            dic = {
                'name': _i.split('?')[0],
                'price': price,
                'timestamp': self.get_time(),
                'url': url
            }
            index_arr.append(dic)

        crypto_arr = []
        for _c in self.cryptos:
            url = self.crypto_url[0]+_c
            price = self.get_crypto_price(url)
            if price:
                dic = {
                    'name': _c.split('?')[0],
                    'price': price,
                    'timestamp': self.get_time(),
                    'url': url
                }
                crypto_arr.append(dic)

        future_arr = []
        for _f in self.futures:
            url = self.future_url[0]+_f
            price = self.get_future_price(url)
            if price:
                dic = {
                    'name': _f.split('?')[0],
                    'price': price,
                    'timestamp': self.get_time(),
                    'url': url
                }
                future_arr.append(dic)
        
        self.save_to_csv(index_arr, crypto_arr, future_arr)
        
    
    @staticmethod
    def get_time():
        dt = pendulum.now()
        return dt.format('DD-MM-YYYYTHH:mm:ss')

    def get_page_content(self, url):
        try:
            self.utils._debug("Trying to get web content for url: "+url)
            response = requests.get(url)
            return response
        except ConnectionError as e:
            self.utils._error("Cannot get web page: "+str(e))
            exit(1)

    def save_to_csv(self, index_arr, crypto_arr, future_arr):
        dt = pendulum.now()
        _i = index_arr[0].keys()
        file_name = 'indexes_{}.csv'.format(dt.format('YYYYMMDD'))
        file_path = Path(self.cfg['target']+"indexes"+file_name)
        if file_path.is_file():
            with open(file_name, 'a', newline='')  as output_file:
                dict_writer = csv.DictWriter(output_file, _i, delimiter="`")
                dict_writer.writerows(index_arr)
        else:
            with open(file_name, 'w', newline='')  as output_file:
                dict_writer = csv.DictWriter(output_file, _i, delimiter="`")
                dict_writer.writeheader()
                dict_writer.writerows(index_arr)

        _c = crypto_arr[0].keys()
        file_name = 'crypto_{}.csv'.format(dt.format('YYYYMMDD'))
        file_path = Path(self.cfg['target']+"cryptos"+file_name)
        if file_path.is_file():
            with open(file_name, 'a', newline='')  as output_file:
                dict_writer = csv.DictWriter(output_file, _c, delimiter="`")
                dict_writer.writerows(crypto_arr)
        else:
            with open(file_name, 'w', newline='')  as output_file:
                dict_writer = csv.DictWriter(output_file, _c, delimiter="`")
                dict_writer.writeheader()
                dict_writer.writerows(crypto_arr)

        _f = future_arr[0].keys()
        file_name = 'future_{}.csv'.format(dt.format('YYYYMMDD'))
        file_path = Path(self.cfg['target']+"futures"+file_name)
        if file_path.is_file():
            with open(file_name, 'a', newline='')  as output_file:
                dict_writer = csv.DictWriter(output_file, _f, delimiter="`")
                dict_writer.writerows(future_arr)
        else:
            with open(file_name, 'w', newline='')  as output_file:
                dict_writer = csv.DictWriter(output_file, _f, delimiter="`")
                dict_writer.writeheader()
                dict_writer.writerows(future_arr)
        




    '''
        name: get_stock_price
        args: s - stock short name
        desc: get web page content from link in config parametr 'url'
              and parse it by tags 'h3' > 'bg-quote'
    '''
    #TODO: tag changes
    # def get_stock_price(self, s):
    #     url = self.url+s
    #     response = self.get_page_content(url)
    #     try:
    #         soup = BeautifulSoup(response.content, 'html.parser')
    #         result = soup.find_all('h3', class_='intraday__price')
    #         for i in result:
    #             price = i.find('bg-quote', class_='value')
    #             self.utils._debug("Price for {}: {}".format(s.upper(), price.text))
    #         if price:
    #             return float(price.text.replace(',', ''))
    #         else:
    #             self.utils._error("Cannot obtain price from web page")
    #             return None
    #     except Exception as e:
    #         self.utils._error("Cannot obtain price from web page: "+str(e))
    #         return None 
    
    def get_index_price(self, url):
        response = self.get_page_content(url)
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            price = None
            self.utils._debug("Start parsing")
            if 'businessinsider' in url:
                result = soup.find_all('div', class_='price-section__values')
                for i in result:
                    price = i.find('span', class_='price-section__current-value')
                    self.utils._debug("Price for FTSE All world: {}".format( price.text))
            else:
                result = soup.find_all('h3', class_='intraday__price')
                for i in result:
                    price = i.find('span', class_='value')
                    self.utils._debug("Price from {}: {}".format(url, price.text))
            if price:
                return float(price.text.replace(',', ''))
            else:
                self.utils._error("Cannot obtain price from web page")
                return None
        except Exception as e:
            self.utils._error("Cannot obtain price from web page: "+str(e))
    
    def get_crypto_price(self, url):
        response = self.get_page_content(url)
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            self.utils._debug("Start parsing")
            result = soup.find_all('h3', class_='intraday__price')
            for i in result:
                self.utils._debug("Price from {}: {}".format(url, price.text))
                price = i.find('bg-quote', class_='value')
            if price:
                return float(price.text.replace(',', ''))
            else:
                self.utils._error("Cannot obtain price from web page")
                return None
        except Exception as e:
            self.utils._error("Cannot obtain price from web page: "+str(e))
    
    def get_future_price(self, url):
        response = self.get_page_content(url)
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            self.utils._debug("Start parsing")
            result = soup.find_all('h3', class_='intraday__price')
            for i in result:
                tag = 'bg-quote' if 'es00' in url else 'span'
                price = i.find(tag, class_='value')
                self.utils._debug("Price from {}: {}".format(url, price.text))
            if price:
                return float(price.text.replace(',', ''))
            else:
                self.utils._error("Cannot obtain price from web page")
                return None
        except Exception as e:
            self.utils._error("Cannot obtain price from web page: "+str(e))

    # @staticmethod
    def time_check(self):
        _result_hour = True
        _result_day = True
        dt=pendulum.now()
        if dt.hour < 15 or dt.hour > 23:
            _result_hour = False
        if dt.isoweekday in [6,7]:
            _result_day = False
        self.utils._debug('_result_hour: '+str(_result_hour))
        self.utils._debug('_result_day: '+str(_result_day))
        return _result_day and _result_hour    
        
        #TODO: check if trades are started


if __name__ == '__main__':
    WebParser()
    