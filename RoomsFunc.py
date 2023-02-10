import re


def description_olx_scraping(soup):
    additional_fees = 0
    try:
        description = soup.select('.css-bgzo2k.er34gjf0')[0].text
    except IndexError:
        return -1
    description = description.lower()
    sentences = re.split(r'[.\n+]', description)
    description_to_re = ''
    unwanted_words = ['kaucj', 'opcjonaln', 'gara']
    flag = True
    for sentence in sentences:
        for unwanted_word in unwanted_words:
            if unwanted_word in sentence:
                flag = False
                break
        if flag:
            description_to_re += sentence
        flag = True
    mo = r"(\d+\s?,?\d+(zł|zl| zł| zl|pln| pln|koszty| koszty|czynsz| czynsz))"
    bills = re.findall(mo, description_to_re)
    bills = ["".join(x) for x in bills]

    for j in range(len(bills)):
        bills[j] = ''.join(x for x in bills[j] if x.isdigit())
    bills[:] = list(set(bills))
    bills[:] = [float(x) for x in list(set(bills)) if float(x) < 600]
    for bill in bills:
        additional_fees += bill
    return additional_fees


def tags_olx_scraping(soup):
    tags = soup.select('li.css-1r0si1e')
    for tag in tags:
        if "Rodzaj pokoju:" in tag.text:
            return tag.text[15:]

    return "unknown"


def olx_or_otodom(ad):
    olx_ad = []
    for name in ad:
        if "otodom" not in name['href']:
            olx_ad.append("https://www.olx.pl" + name['href'])
        else:
            olx_ad.append(name['href'])
    return olx_ad
