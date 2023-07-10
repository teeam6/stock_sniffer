import os, sys, json, requests, hashlib, csv, pendulum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP, BIGINT, Boolean, Float

Base = declarative_base()

class Stock(Base):
    __tablename__ = "stock"
    id = Column(Integer, primary_key=True, autoincrement=True)
    meta_id = Column(Integer)
    price = Column(Float)
    created_at = Column(TIMESTAMP)

    def __init__(self, meta_id,
                 price=None,
                 created_at=None):
        self.meta_id = meta_id
        self.price = price
        self.created_at = created_at


class Index(Base):
    __tablename__ = "index"
    id = Column(Integer, primary_key=True, autoincrement=True)
    meta_id = Column(Integer)
    price = Column(Float)
    created_at = Column(TIMESTAMP)

    def __init__(self, meta_id,
                 price=None,
                 created_at=None):
        self.meta_id = meta_id
        self.price = price
        self.created_at = created_at


class Future(Base):
    __tablename__ = "future"
    id = Column(Integer, primary_key=True, autoincrement=True)
    meta_id = Column(Integer)
    price = Column(Float)
    created_at = Column(TIMESTAMP)

    def __init__(self, meta_id,
                 price=None,
                 created_at=None):
        self.meta_id = meta_id
        self.price = price
        self.created_at = created_at


class Crypto(Base):
    __tablename__ = "crypto"
    id = Column(Integer, primary_key=True, autoincrement=True)
    meta_id = Column(Integer)
    price = Column(Float)
    created_at = Column(TIMESTAMP)

    def __init__(self, meta_id,
                 price=None,
                 created_at=None):
        self.meta_id = meta_id
        self.price = price
        self.created_at = created_at


class Meta(Base):
    __tablename__ = "meta"
    id = Column(Integer, primary_key=True, autoincrement=True)
    m_type = Column(String)
    m_name = Column(String)
    m_code = Column(String)
    m_curr = Column(String)
    m_url = Column(String)
    m_open = Column(TIMESTAMP)
    m_close = Column(TIMESTAMP)

    def __init__(self, m_type,
                 m_name,
                 m_code,
                 m_curr,
                 m_url,
                 m_open=None,
                 m_close=None):
        _m_type = ['stock','future','index','crypto']
        if m_type not in _m_type:
            raise ValueError(f"Type value have to be one of {_m_type} not {m_type}")
        
        self.m_type = m_type
        self.m_name = m_name
        self.m_code = m_code
        self.m_curr = m_curr
        self.m_url = m_url
        self.m_open = m_open
        self.m_close = m_close

# class Stock:
#     def __init__(self, entity: str, url: str, timestamp: str):
#         self.url  = f"{url}/{entity}"
#         self.timestamp = timestamp
#         self._price = None

#     @property
#     def price(self):
#         return self._price
    
#     @price.setter
#     def price(self, price):
#         if type(price) is float or type(price) is int:
#             self._price = float(price)
#         else:
#             raise ValueError(f"Price could be only float or int: {type(price)}")

# class Index:
#     def __init__(self, entity: str, url: str, timestamp: str):
#         self.url  = f"{url}/{entity}"
#         self.timestamp = timestamp
#         self._price = None

#     @property
#     def price(self):
#         return self._price
    
#     @price.setter
#     def price(self, price):
#         if type(price) is float or type(price) is int:
#             self._price = float(price)
#         else:
#             raise ValueError(f"Price could be only float or int: {type(price)}")


# class Future:
#     def __init__(self, entity: str, url: str, timestamp: str):
#         self.url  = f"{url}/{entity}"
#         self.timestamp = timestamp
#         self._price = None

#     @property
#     def price(self):
#         return self._price
    
#     @price.setter
#     def price(self, price):
#         if type(price) is float or type(price) is int:
#             self._price = float(price)
#         else:
#             raise ValueError(f"Price could be only float or int: {type(price)}")

# class Crypto:
#     def __init__(self, entity: str, url: str, timestamp: str):
#         self.url  = f"{url}/{entity}"
#         self.timestamp = timestamp
#         self._price = None

#     @property
#     def price(self):
#         return self._price
    
#     @price.setter
#     def price(self, price):
#         if type(price) is float or type(price) is int:
#             self._price = float(price)
#         else:
#             raise ValueError(f"Price could be only float or int: {type(price)}")