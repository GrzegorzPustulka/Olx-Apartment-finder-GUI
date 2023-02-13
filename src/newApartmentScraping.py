from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
import pandas as pd
from emailSender import email_sender
import time
from ApartmentFunc import *


@dataclass
class Ads:
    link: str
    area: str
    rooms: str
    price: float
    rent: float
    total: float


def new_apartments_scraping(max_price, min_price, link, our_districts):
    previous_ad = ''
    ads = []
    sender = '**********'
    email_password = '**********'
    receiver = '**********'
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

        price = soup.find_all("p", attrs={"data-testid": "ad-price"})[3].text.replace(' ', '').replace(',', '.').replace(',', '.').replace('zł', '')
        price = float(price)

        if district in our_districts and max_price >= price >= min_price:
            req = requests.get(ad)
            soup = BeautifulSoup(req.text, 'lxml')
            if "olx.pl" in ad:
                olx_rent, olx_area, olx_rooms = tags_olx_scraping(soup)
            else:
                olx_rent = rent_otodom_scraping(soup)
                olx_area = area_otodom_scraping(soup)
                olx_rooms = '?'

            if max_price >= price + olx_rent >= min_price and ad != previous_ad:
                previous_ad = ad
                offer = Ads(ad, olx_area, olx_rooms, price, olx_rent, price + olx_rent)
                ads.append(offer)
                df = pd.DataFrame(ads)
                print(df)
                df.to_excel('newApartments.xlsx')
                email_sender(str(offer), sender, email_password, receiver)

        time.sleep(30)

