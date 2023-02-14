from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
import threading
import pandas as pd
from RoomsFunc import *


@dataclass
class Ads:
    link: str
    room: str
    price: float
    bills: float
    total: float


ads = []
lock = threading.Lock()


def all_rooms_scraping(max_price, min_price, link, our_districts, room):
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

    for i, district in enumerate(olx_districts):
        for name in our_districts:
            if name in district.text:
                if max_price >= olx_prices[i] >= min_price:
                    req = requests.get(olx_ad[i])
                    soup = BeautifulSoup(req.text, 'lxml')
                    if "olx.pl" in olx_ad[i]:
                        additional_fees = description_olx_scraping(soup)
                        if additional_fees == -1:
                            break
                        else:
                            type_room = tags_olx_scraping(soup)
                    else:
                        additional_fees = rent_otodom_scraping(soup)
                        type_room = room_otodom_scraping(soup)
                    if max_price >= olx_prices[i] + additional_fees >= min_price and (type_room == 'unknown' or type_room == room):
                        ad = Ads(olx_ad[i], type_room, olx_prices[i], additional_fees, olx_prices[i] + additional_fees)
                        with lock:
                            ads.append(ad)


def run_all_rooms(max_price, min_price, link, our_districts, room):
    threads = []
    req = requests.get(link)
    soup = BeautifulSoup(req.text, 'lxml')
    count_pages = int(soup.select('li[data-testid="pagination-list-item"]')[3].text)

    for i in range(count_pages):
        if i == 0:
            t = threading.Thread(target=all_rooms_scraping, args=(max_price, min_price, link, our_districts, room))
            threads.append(t)
            t.start()
        else:
            t = threading.Thread(target=all_rooms_scraping, args=(max_price, min_price, link + "?page=" + str(i + 1), our_districts, room))
            threads.append(t)
            t.start()

    for thread in threads:
        thread.join()

    df = pd.DataFrame(ads)
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    print(df)
    df.to_excel('AllRoom.xlsx')
