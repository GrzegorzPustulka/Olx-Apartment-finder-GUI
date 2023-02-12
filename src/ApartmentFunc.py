import re


def tags_olx_scraping(soup):
    olx_rent = 0
    olx_area = 'unknown'
    olx_rooms = 'unknown'
    tags = soup.select('li.css-1r0si1e')
    for tag in tags:
        if "Czynsz" in tag.text:
            text_prices = tag.text.replace(' ', '').replace(',', '.')
            olx_rent = (int(re.findall(r'\d+', text_prices)[0]))
        elif "Powierzchnia" in tag.text:
            olx_area = tag.text[14:]
        elif "Liczba pokoi: " in tag.text:
            olx_rooms = tag.text[14:]
    return olx_rent, olx_area, olx_rooms


def rent_otodom_scraping(soup):
    tags = soup.find_all('script')
    match = (r'"key":"rent","value":"(\d+)"')

    if len(re.findall(match, tags[-1].text)) == 0:
        olx_rent = 0
    else:
        olx_rent = int(re.findall(match, tags[-1].text)[0])

    return olx_rent


def area_otodom_scraping(soup):
    tags = soup.find_all('script')
    match = (r'"key":"m","value":"(\d+.?\d+)"')

    if len(re.findall(match, tags[-1].text)) == 0:
        olx_area = 'unknown'
    else:
        olx_area = re.findall(match, tags[-1].text)[0] + " m²"

    return olx_area


def olx_or_otodom(ad):
    olx_ad = []
    for name in ad:
        if "otodom" not in name['href']:
            olx_ad.append("https://www.olx.pl" + name['href'])
        else:
            olx_ad.append(name['href'])
    return olx_ad

