import json
import re
from datetime import datetime, timedelta, timezone

import requests
from bs4 import BeautifulSoup

def main():
    utc_plus_3 = timezone(timedelta(hours=3))
    snapshot = {
        'timestamp': datetime.now(utc_plus_3).strftime("%Y-%m-%d %H:%M:%S"),
        'offers': [],
    }
    page = requests.get('https://funpay.com/lots/81/').text
    soup = BeautifulSoup(page, 'html.parser')
    for a in soup.find(class_='tc table-hover table-clickable tc-short showcase-table tc-lazyload tc-sortable showcase-has-promo').find_all(recursive=False):
        if a.get('data-f-type1') == 'продажа' and a.get('data-f-type') == 'с рейтингом' and (int(a.get('data-f-solommr')) > 5620 if a.get('data-f-solommr') else False):
            # print(a.prettify())
            snapshot['offers'].append({
                'title': a.find('div', class_='tc-desc-text').string,
                'link': a.get('href'),
                'price': float(a.find('div', class_='tc-price').get('data-s')),
                'seller_link': a.find('div', class_='avatar-photo').get('data-href'),
                'seller_name': a.find('div', class_='media-user-name').string[1:],
                'seller_image_url': re.search(r'url\((.*)\);', a.find('div', class_='avatar-photo').get('style')).group(1),
                'mmr': int(a.get('data-f-solommr')),
                'time': int(a.get('data-f-time')),
                'decency': int(a.get('data-f-decency')) if a.get('data-f-decency') else None,
            })
    # print(len(snapshot['offers']))
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    # data['snapshots'] = []
    data['snapshots'].append(snapshot)
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

main()