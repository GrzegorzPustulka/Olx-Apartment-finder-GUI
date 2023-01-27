from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


@dataclass
class Ads:
    link: str
    price: float
    rent: float
    total: float


def all_apartments_scraping(max_price, min_price, link, our_districts):
    ads = []
    req = requests.get(link)
    soup = BeautifulSoup(req.text, 'lxml')
    # count pages
    count_pages = int(soup.select('li[data-testid="pagination-list-item"]')[3].text)

    for page_number in range(1, count_pages):
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
        buffer = []
        for i in olx_buffer_prices:
            buffer.append(i.text)
        text_prices = ''
        for price in buffer:
            text_prices += price
        text_prices = text_prices.replace(' ', '').replace(',', '.')
        olx_prices = [float(x) for x in re.findall(r'\d*\.\d+|\d+', text_prices)]

        olx_rent = 0
        for i, district in enumerate(olx_districts):
            for name in our_districts:
                if name in district.text:
                    if max_price >= olx_prices[i] >= min_price:
                        req = requests.get(olx_ad[i])
                        soup = BeautifulSoup(req.text, 'lxml')

                        if "olx.pl" in olx_ad[i]:
                            price_rent_buffer = soup.select('li.css-1r0si1e')
                            for k in price_rent_buffer:
                                if "Czynsz" in k.text:
                                    text_prices = k.text.replace(' ', '').replace(',', '.')
                                    olx_rent = (int(re.findall(r'\d+', text_prices)[0]))
                        else:
                            olx_rent = 0
                        if max_price >= olx_prices[i] + olx_rent >= min_price:
                            ad = Ads(olx_ad[i], olx_prices[i], olx_rent, olx_prices[i] + olx_rent)
                            ads.append(ad)
                        break

        req = requests.get(link + "?page=" + str(page_number+1))
        soup = BeautifulSoup(req.text, 'lxml')

    df = pd.DataFrame(ads)
    print(df)
    df.to_excel('AllApartments.xlsx')
