import requests  as rq
import pandas as pd
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

urls = []

for i in range(1, 47):
    url = f"https://mai.ru/press/news/?tags=1235&PAGEN_1={i}"

    urls.append(url)

data = {
    "title": [],
    "date": []
}

for url in urls:
    response = rq.get(url, verify=False)

    if response:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        items = soup.select('a.card')

        for item in items:
            titles = item.find('h5').text.strip()
            dates = item.select_one('span.badge').text.strip()

            date = item.select_one('span.badge')

            data['title'].append(titles)
            data['date'].append(dates)

    else:
        print(f"Error: {response.status_code}")

df = pd.DataFrame(data)

months = {
    'янв': '01',
    'фев': '02',
    'мар': '03',
    'апр': '04',
    'мая': '05',
    'июн': '06',
    'июл': '07',
    'авг': '08',
    'сен': '09',
    'окт': '10',
    'ноя': '11',
    'дек': '12'
}

df['date'] = df['date'].replace(months, regex=True)

df["date"] = df["date"].apply(
    lambda x: x + ' 2026' if len(x.split()) == 2 else x
)

df['date'] = pd.to_datetime(df['date'], format='%d %m %Y')

df['date'] = df["date"].dt.strftime('%Y-%m')

df.to_csv('mai_news.csv', index=False)