from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
import threading
import re
import pandas as pd


@dataclass
class Ads:
    link: str
    price: float
    bills: float
    probably: float


ads = []


def all_rooms_scraping(max_price, min_price, link, our_districts):

    thread_ads = []
    req = requests.get(link)
    soup = BeautifulSoup(req.text, 'lxml')
    ad = soup.select("a.css-rc5s2u")
    olx_ad = []
    for name in ad:
        if "otodom" not in name['href']:
            olx_ad.append("https://www.olx.pl" + name['href'])
        else:
            olx_ad.append(name['href'])

    # ad districts from olx 0-51
    olx_districts = soup.find_all("p", attrs={"data-testid": "location-date"})

    # ad price from olx 0-51
    olx_buffer_prices = soup.find_all("p", attrs={"data-testid": "ad-price"})

    # change prices from ad to friendly number
    text_prices = ''.join(i.text.replace(' ', '').replace(',', '.') for i in olx_buffer_prices)
    olx_prices = [float(x) for x in re.findall(r'\d*\.\d+|\d+', text_prices)]

    additional_fees = 0.0
    for i, district in enumerate(olx_districts):
        for name in our_districts:
            if name in district.text:
                if max_price >= olx_prices[i] >= min_price:
                    req = requests.get(olx_ad[i])
                    soup = BeautifulSoup(req.text, 'lxml')

                    if "olx.pl" in olx_ad[i]:
                        description = soup.select('.css-bgzo2k.er34gjf0')[0].text
                        mo = r"(\d+[-,\s-]*\d*zł|\d+złoty|\d+zł|\d+[-,\s-]*\d* PLN|\d+pln|\d+[-,\s-]*\d* zl)"
                        bills = re.findall(mo, description)
                        for j in range(len(bills)):
                            bills[j] = ''.join(x for x in bills[j] if x.isdigit())
                        bills[:] = list(set(bills))
                        bills[:] = [float(x) for x in list(set(bills)) if float(x) < 600]
                        for bill in bills:
                            additional_fees += bill
                    else:
                        additional_fees = 0.0

                    if max_price >= olx_prices[i] >= min_price:
                        ad = Ads(olx_ad[i], olx_prices[i], additional_fees, olx_prices[i] + additional_fees)
                        thread_ads.append(ad)
                    additional_fees = 0.0
    ads.append(thread_ads)


def run_all_rooms(max_price, min_price, link, our_districts):
    threads = []
    req = requests.get(link)
    soup = BeautifulSoup(req.text, 'lxml')
    count_pages = int(soup.select('li[data-testid="pagination-list-item"]')[3].text)

    for i in range(count_pages):
        if i == 0:
            t = threading.Thread(target=all_rooms_scraping, args=(max_price, min_price, link, our_districts))
            threads.append(t)
            t.start()
        else:
            link = link + "?page=" + str(i + 1)
            t = threading.Thread(target=all_rooms_scraping, args=(max_price, min_price, link, our_districts))
            threads.append(t)
            t.start()

    for thread in threads:
        thread.join()

    final_results = []
    for ad in ads:
        final_results.extend(ad)

    df = pd.DataFrame(final_results)
    print(df)
    df.to_excel('AllRoom.xlsx')
