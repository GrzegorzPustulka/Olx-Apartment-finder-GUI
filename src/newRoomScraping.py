from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
from emailSender import email_sender
import pandas as pd
import time
from RoomsFunc import *


@dataclass
class Ads:
    link: str
    room: str
    price: float
    bills: float
    probably: float


def new_room_scraping(max_price, min_price, link, our_districts):
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

        # price
        price = soup.find_all("p", attrs={"data-testid": "ad-price"})[3].text.replace(' ', '').replace(',', '.').replace(',', '.').replace('zł', '')
        price = float(price)

        if district in our_districts and max_price >= price >= min_price:
            req = requests.get(ad)
            soup = BeautifulSoup(req.text, 'lxml')
            if "olx.pl" in ad:
                additional_fees = description_olx_scraping(soup)
                if additional_fees == -1:
                    break
                else:
                    type_room = tags_olx_scraping(soup)
            else:
                additional_fees = 0.0
                type_room = '0'

            if max_price >= price >= min_price and ad != previous_ad:
                previous_ad = ad
                offer = Ads(ad, type_room, price, additional_fees, price + additional_fees)
                ads.append(offer)
                df = pd.DataFrame(ads)
                print(df)
                df.to_excel('newRooms.xlsx')
                email_sender(str(offer), sender, email_password, receiver)

        time.sleep(30)

