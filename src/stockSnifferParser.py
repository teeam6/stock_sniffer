#DB imports
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, or_, not_
from model import Meta, Stock, Index, Future, Crypto
from lib.dbConnector import DBConnector
#SYS imports
import os, sys, pendulum, time
from bs4 import BeautifulSoup
from lib.utils import Utils
import asyncio
import aiohttp
'''
SYS EXIT CODES:
55 - Meta table is empty
60 - Insert error
1 - Unexpected error
0 - Success
'''
class ParsedEntity:
    def __init__(self, entity) -> None:
        self.meta = entity
        self.response = None
        self.price = None

class StockSnifferParser:
    def __init__(self) -> None:
        self.utils = Utils()
        self.now = pendulum.now()
        self.cfg = self.utils.cfg
        self.dbConn = self.init_db()
        self._error = self.utils._error
        self._log = self.utils._log
        self._success = self.utils._success
        self.results = []
        self.errors = []

    def init_db(self):
        try:
            return  DBConnector(self.cfg['database.conn_string'])
        except Exception as e:
            msg = f"Failed establish db connection: {str(e)}"
            self.errors.append(msg)
            self.utils._error(msg)


    def init_worflow(self):
        metas = self.get_metas()
        entities = []
        for meta in metas:
            entities.append(ParsedEntity(meta))

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError as e:
            self.utils._log("There is no event loop running..")
            loop=asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.run_until_complete(self.main(entities))

        self.insert_to_db_results()


    def get_metas(self):
        try:
            _metas = self.dbConn.session.query(Meta).all()
            if len(_metas) == 0:
                raise NoResultFound
            return _metas
        except NoResultFound as e:
            self._error("Meta table is empty. Run init.sql first. Exitting..")
            sys.exit(55)
        except Exception as e:
            self._error(f"Unexpected error exception due meta rows obtaining: {str(e)} \nExitting..")
            sys.exit(1)

    def insert_to_db_results(self):
        now = pendulum.now()
        try:
            for p_meta in self.results:
                try:
                    if p_meta.meta.m_type == 'future':
                        obj = Future(meta_id= p_meta.meta.id, price=p_meta.price, created_at=now)
                    elif p_meta.meta.m_type == 'stock':
                        obj = Stock(meta_id= p_meta.meta.id, price=p_meta.price, created_at=now)
                    elif p_meta.meta.m_type == 'index':
                        obj = Index(meta_id= p_meta.meta.id, price=p_meta.price, created_at=now)
                    elif p_meta.meta.m_type == 'crypto':
                        obj = Crypto(meta_id= p_meta.meta.id, price=p_meta.price, created_at=now)
                except Exception as e:
                    msg = f"Cannot insert to some table: {str(e)}"
                    self.errors.append(msg)
                    self.utils._error(msg)
                    continue

                self.dbConn.add_record(obj)
                self.dbConn.session.commit()
        except Exception as e:
            self._error(f"Cannot insert to PSQL table: {str(e)}. Exitting..")
            sys.exit(60)

    async def get_response(self, session, p_meta):
        async with session.get(p_meta.meta.m_url) as response:
            p_meta.response = await response.text()
            return p_meta
    
    async def main(self, metas):
        tasks = []
        async with aiohttp.ClientSession() as session:
            for meta in metas:
                tasks.append(self.get_response(session, meta))
            results = await asyncio.gather(*tasks)
            for p_meta in results:
                if p_meta.meta.m_type == 'future':
                    result = self.get_future_price(p_meta)
                elif p_meta.meta.m_type == 'stock':
                    result = self.get_stock_price(p_meta)
                elif p_meta.meta.m_type == 'index':
                    result = self.get_index_price(p_meta)
                elif p_meta.meta.m_type == 'crypto':
                    result = self.get_crypto_price(p_meta)
                self.results.append(result)

    def get_future_price(self, meta):
        try:
            tag=None
            soup = BeautifulSoup(meta.response, 'html.parser')
            price = None
            result = soup.find_all('h2', class_='intraday__price')
            for i in result:
                try:
                    tag = 'span'
                    price = i.find(tag, class_='value')
                    self.utils._warning("Price from {}: {}".format(meta.meta.m_url, price.text))
                except Exception as e:
                    tag = 'bg-quote'
                    price = i.find(tag, class_='value')
                    self.utils._warning("Price from {}: {}".format(meta.meta.m_url, price.text))
            if price:
                meta.price=float(price.text.replace(',', ''))
                return meta
            else:
                with open(file=f'/var/log/stock_sniffer/future_errors_{self.now.strftime("%Y%m%d")}', mode='a+') as f:
                    f.write(f'Called: {meta.meta.m_url}\tSearched for:{tag}\t{self.now.strftime("%Y%m%dT%H%M")}\n')
                    f.write(meta.response+'\n')
                msg = "Cannot obtain price from web page"
                self.errors.append(msg)
                self.utils._error(msg)
                return None
        except Exception as e:
            with open(file=f'/var/log/stock_sniffer/future_errors_{self.now.strftime("%Y%m%d")}', mode='a+') as f:
                f.write(f'Called: {meta.meta.m_url}\tSearched for:{tag}\t{self.now.strftime("%Y%m%dT%H%M")}\n')
                f.write(meta.response+'\n')
            msg = "Cannot obtain price from web page: "+str(e)
            self.errors.append(msg)
            self.utils._error(msg)
    
    def get_stock_price(self, meta):
        try:
            tag=None
            soup = BeautifulSoup(meta.response, 'html.parser')
            result = soup.find_all('h2', class_='intraday__price')
            price=None
            for i in result:
                price = i.find('bg-quote', class_='value')
                self.utils._warning("Price from {}: {}".format(meta.meta.m_url, price.text))
            if price:
                meta.price=float(price.text.replace(',', ''))
                return meta
            else:
                msg = "Cannot obtain price from web page"
                self.errors.append(msg)
                self.utils._error(msg)

                with open(file=f'/var/log/stock_sniffer/stock_errors_{self.now.strftime("%Y%m%d")}', mode='a+') as f:
                    f.write(f'Called: {meta.meta.m_url}\tSearched for:{tag}\t{self.now.strftime("%Y%m%dT%H%M")}\n')
                    f.write(meta.response+'\n')
                return None
        except Exception as e:
            with open(file=f'/var/log/stock_sniffer/stock_errors_{self.now.strftime("%Y%m%d")}', mode='a+') as f:
                f.write(f'Called: {meta.meta.m_url}\tSearched for:{tag}\t{self.now.strftime("%Y%m%dT%H%M")}\n')
                f.write(meta.response+'\n')
            msg = "Cannot obtain price from web page: "+str(e)
            self.errors.append(msg)
            self.utils._error(msg)

            return None 
    
    def get_index_price(self, meta):
        try:
            tag=None
            soup = BeautifulSoup(meta.response, 'html.parser')
            price = None
            if 'businessinsider' in meta.meta.m_url:
                result = soup.find_all('div', class_='price-section__values')
                for i in result:
                    price = i.find('span', class_='price-section__current-value')
                    self.utils._warning("Price from {}: {}".format(meta.meta.m_url, price.text))
            elif 'cnbc.com' in meta.meta.m_url:
                price = soup.find('span', class_='QuoteStrip-lastPrice')
                self.utils._warning("Price from {}: {}".format(meta.meta.m_url, price.text))                    
            else:
                result = soup.find_all('h2', class_='intraday__price')
                for i in result:
                    try:
                        tag = 'span'
                        price = i.find(tag, class_='value')
                        self.utils._warning("Price from {}: {}".format(meta.meta.m_url, price.text))
                    except Exception as e:
                        tag = 'bg-quote'
                        price = i.find(tag, class_='value')
                        self.utils._warning("Price from {}: {}".format(meta.meta.m_url, price.text))
            if price:
                meta.price=float(price.text.replace(',', ''))
                return meta
            else:
                msg = "Cannot obtain price from web page"
                self.errors.append(msg)
                self.utils._error(msg)

                with open(file=f'/var/log/stock_sniffer/index_errors_{self.now.strftime("%Y%m%d")}', mode='a+') as f:
                    f.write(f'Called: {meta.meta.m_url}\tSearched for:{tag}\t{self.now.strftime("%Y%m%dT%H%M")}\n')
                    f.write(meta.response+'\n')
                return None
        except Exception as e:
            with open(file=f'/var/log/stock_sniffer/index_errors_{self.now.strftime("%Y%m%d")}', mode='a+') as f:
                f.write(f'Called: {meta.meta.m_url}\tSearched for:{tag}\t{self.now.strftime("%Y%m%dT%H%M")}\n')
                f.write(meta.response+'\n')
            msg = "Cannot obtain price from web page: "+str(e)
            self.errors.append(msg)
            self.utils._error(msg)
    
    def get_crypto_price(self, meta):
        try:
            tag=None
            soup = BeautifulSoup(meta.response, 'html.parser')
            price = None
            result = soup.find_all('h2', class_='intraday__price')
            for i in result:
                price = i.find('bg-quote', class_='value')
                self.utils._warning("Price from {}: {}".format(meta.meta.m_url, price.text))
            if price:
                meta.price=float(price.text.replace(',', ''))
                return meta
            else:
                msg="Cannot obtain price from web page"
                self.errors.append(msg)
                self.utils._error(msg)

                with open(file=f'/var/log/stock_sniffer/crypto_errors_{self.now.strftime("%Y%m%d")}', mode='a+') as f:
                    f.write(f'Called: {meta.meta.m_url}\tSearched for:{tag}\t{self.now.strftime("%Y%m%dT%H%M")}\n')
                    f.write(meta.response+'\n')
                return None
        except Exception as e:
            with open(file=f'/var/log/stock_sniffer/crypto_errors_{self.now.strftime("%Y%m%d")}', mode='a+') as f:
                f.write(f'Called: {meta.meta.m_url}\tSearched for:{tag}\t{self.now.strftime("%Y%m%dT%H%M")}\n')
                f.write(meta.response+'\n')
            msg="Cannot obtain price from web page: "+str(e)
            self.errors.append(msg)
            self.utils._error(msg)

    def send_report(self):
        if self.errors:
            msg = f"Ended with errors: \n"
            for i in self.errors:
                msg += f"{i} \n"
        else:
            return
        cmd = f"python3 /opt/serger/src/notifier.py -m '{msg}'"
        self.utils._warning(f"Executing command: {cmd}")
        try:
            os.system(cmd)
        except Exception as e:
            self.utils._error(f"Cannot send notification: {str(e)}")
    

if __name__ == '__main__':
    script_start = time.monotonic()

    parser = StockSnifferParser()
    parser.init_worflow()
    if parser.cfg['general.notify']:
        parser.utils._warning("Notification option is on")
        parser.send_report()
    else:
        parser.utils._warning("Notification option is off")

    script_end = time.monotonic()
    parser._success(f'Parsing done in {script_end - script_start}..')
