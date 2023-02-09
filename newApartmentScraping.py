from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from emailSender import email_sender
import time


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
    email = input('Enter email: ')
    password = input('Enter password: ')
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

        olx_rent = 0
        olx_area = '0'
        olx_rooms = '0'
        if district in our_districts and max_price >= price >= min_price:
            req = requests.get(ad)
            soup = BeautifulSoup(req.text, 'lxml')
            if "olx.pl" in ad:
                tags = soup.select('li.css-1r0si1e')
                for tag in tags:
                    if "Czynsz" in tag.text:
                        text_prices = tag.text.replace(' ', '').replace(',', '.')
                        olx_rent = (int(re.findall(r'\d+', text_prices)[0]))
                    elif "Powierzchnia" in tag.text:
                        olx_area = tag.text[14:]
                    elif "Liczba pokoi:" in tag.text:
                        olx_rooms = tag.text[14:]
            else:
                olx_rent = 0
                olx_area = '0'
                olx_rooms = '0'

            if max_price >= price + olx_rent >= min_price and ad != previous_ad:
                previous_ad = ad
                offer = Ads(ad, olx_area, olx_rooms, price, olx_rent, price + olx_rent)
                ads.append(offer)
                df = pd.DataFrame(ads)
                print(df)
                df.to_excel('newApartments.xlsx')
                email_sender(offer, email, password)

        time.sleep(30)

