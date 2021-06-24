import os, sys, json, requests, hashlib, csv, pendulum
from lib.utils import Utils
from pydantic import BaseModel

class Stock(BaseModel):
    short: str
    price: float
    timestamp: str
    url: str

class Crypto(BaseModel):
    name: str
    price: float
    timestamp: str
    url: str

class Index(BaseModel):
    name: str
    price: float
    timestamp: str
    url: str

class Future(BaseModel):
    name: str
    price: float
    timestamp: str
    url: str
