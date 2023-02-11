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


def olx_or_otodom(ad):
    olx_ad = []
    for name in ad:
        if "otodom" not in name['href']:
            olx_ad.append("https://www.olx.pl" + name['href'])
        else:
            olx_ad.append(name['href'])
    return olx_ad
