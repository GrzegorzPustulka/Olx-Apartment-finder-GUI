from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import threading
from ApartmentFunc import *


@dataclass
class Ads:
    link: str
    area: str
    rooms: str
    price: float
    rent: float
    total: float


ads = []
lock = threading.Lock()


def all_apartments_scraping(max_price, min_price, link, our_districts):
    req = requests.get(link)
    soup = BeautifulSoup(req.text, 'lxml')
    ad = soup.select("a.css-rc5s2u")

    olx_ad = olx_or_otodom(ad)

    # ad districts from olx 0-51
    olx_districts = soup.find_all("p", attrs={"data-testid": "location-date"})

    # ad price from olx 0-51
    olx_buffer_prices = soup.find_all("p", attrs={"data-testid": "ad-price"})

    # change prices from ad to friendly number
    text_prices = ''.join(i.text.replace(' ', '').replace(',', '.') for i in olx_buffer_prices)
    olx_prices = [float(x) for x in re.findall(r'\d*\.\d+|\d+', text_prices)]

    olx_rent = 0
    olx_area = '0'
    olx_rooms = '0'
    for i, district in enumerate(olx_districts):
        for name in our_districts:
            if name in district.text:
                if max_price >= olx_prices[i] >= min_price:
                    req = requests.get(olx_ad[i])
                    soup = BeautifulSoup(req.text, 'lxml')

                    if "olx.pl" in olx_ad[i]:
                        olx_rent, olx_area, olx_rooms = tags_olx_scraping(soup)
                    else:
                        olx_rent = 0
                        olx_area = '?'
                        olx_rooms = '?'
                    if max_price >= olx_prices[i] + olx_rent >= min_price:
                        ad = Ads(olx_ad[i], olx_area, olx_rooms, olx_prices[i], olx_rent, olx_prices[i] + olx_rent)
                        with lock:
                            ads.append(ad)


def run_all_apartments(max_price, min_price, link, our_districts):
    threads = []
    req = requests.get(link)
    soup = BeautifulSoup(req.text, 'lxml')
    count_pages = int(soup.select('li[data-testid="pagination-list-item"]')[3].text)

    for i in range(count_pages):
        if i == 0:
            t = threading.Thread(target=all_apartments_scraping, args=(max_price, min_price, link, our_districts))
            threads.append(t)
            t.start()
        else:
            t = threading.Thread(target=all_apartments_scraping, args=(max_price, min_price, link + "?page=" + str(i + 1), our_districts))
            threads.append(t)
            t.start()

    for thread in threads:
        thread.join()

    df = pd.DataFrame(ads)
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    print(df)
    df.to_excel('AllApartment.xlsx')
