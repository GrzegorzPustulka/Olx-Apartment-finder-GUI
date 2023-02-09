from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
import re
from emailSender import email_sender
import pandas as pd
import time


@dataclass
class Ads:
    link: str
    price: float
    bills: float
    probably: float


def new_room_scraping(max_price, min_price, link, our_districts):
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

        additional_fees = 0.0
        if district in our_districts and max_price >= price >= min_price:
            req = requests.get(ad)
            soup = BeautifulSoup(req.text, 'lxml')
            if "olx.pl" in ad:
                description = soup.select('.css-bgzo2k.er34gjf0')[0].text
                mo = r"(\d+\s?,?\d+(zł|zl| zł| zl|PLN| PLN|ZŁ|ZL| ZŁ| ZL|koszty | koszty))"
                bills = re.findall(mo, description)

                for i in range(len(bills)):
                    bills[i] = ''.join(x for x in bills[i] if x.isdigit())
                bills[:] = list(set(bills))
                bills[:] = [float(x) for x in list(set(bills)) if float(x) < 600]
                for bill in bills:
                    additional_fees += bill
            else:
                additional_fees = 0.0

            if max_price >= price >= min_price and ad != previous_ad:
                previous_ad = ad
                offer = Ads(ad, price, additional_fees, price + additional_fees)
                ads.append(offer)
                df = pd.DataFrame(ads)
                print(df)
                df.to_excel('newRooms.xlsx')
                email_sender(ad, email, password)

        time.sleep(30)

