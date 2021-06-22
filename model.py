import os, sys, json, requests, hashlib, csv, pendulum
from lib.utils import Utils
from pydantic import BaseModel

class Stock(BaseModel):
    short: str
    price: float
    timestamp: str
    url: str

#TODO: crypto, indexes, futures


