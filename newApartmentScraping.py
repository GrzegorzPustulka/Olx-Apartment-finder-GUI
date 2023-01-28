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
    district: str


def new_apartments_scraping(max_price, min_price, link, our_districts):
    previous_ad = ''
    offer_list = []
    while True:
        req = requests.get(link)
        soup = BeautifulSoup(req.text, 'lxml')

        # link
        ad = soup.select("a.css-rc5s2u")[3]['href']
        if "otodom" not in ad:
            ad = "https://www.olx.pl" + ad

        # district
        district = soup.find_all("p", attrs={"data-testid": "location-date"})[3].text
        end_index = district.find(" -")
        district = district[8:end_index]

        # price
        price = soup.find_all("p", attrs={"data-testid": "ad-price"})[3].text.replace(' ', '').replace(',', '.').replace(',', '.').replace('zł', '')
        price = float(price)
        rent = 0

        if district in our_districts and max_price >= price >= min_price:
            req = requests.get(ad)
            soup = BeautifulSoup(req.text, 'lxml')
            if "olx.pl" in ad:
                rent_buffer = soup.select('li.css-1r0si1e')
                for i in rent_buffer:
                    if "Czynsz" in i.text:
                        text_prices = i.text.replace(' ', '').replace(',', '.')
                        rent = (float(re.findall(r'\d+', text_prices)[0]))
            else:
                rent = 0

            if max_price >= price + rent >= min_price and ad != previous_ad:
                previous_ad = ad
                offer = Ads(ad, price, rent, price + rent, district)
                offer_list.append(offer)
                df = pd.DataFrame(offer_list)
                print(df)
                #df.to_excel('AllApartments.xlsx')

        time.sleep(30)

