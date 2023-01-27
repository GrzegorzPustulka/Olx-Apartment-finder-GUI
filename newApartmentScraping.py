from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time


@dataclass
class Ads:
    link: str
    price: float
    rent: float
    total: float


def new_apartments_scraping(max_price, min_price, link, our_districts):
    print("hello")

