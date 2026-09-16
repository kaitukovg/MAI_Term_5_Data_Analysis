import requests as rq
import pandas as pd
from bs4 import BeautifulSoup

urls = []

for i in range(1, 61):
    page = f"https://www.rea.ru/news?tree-content-path=news&search=&date_from=&date_to=&sub%5B0%5D=57407&page={i}&per-page=12"
    urls.append(page)

data = {
    "title": [],
    "date": []
}

for url in urls:
    response = rq.get(url)

    if response:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        titles = soup.select('div.catalog__item-title')
        dates = soup.select('div.catalog__item-date')

        for title, date in zip(titles, dates):
            data["title"].append(title.text.strip())
            data["date"].append(date.text.strip())

    else:
        print(response.status_code)

df = pd.DataFrame(data)

months = {
    'января': '01',
    'февраля': '02',
    'марта': '03',
    'апреля': '04',
    'мая': '05',
    'июня': '06',
    'июля': '07',
    'августа': '08',
    'сентября': '09',
    'октября': '10',
    'ноября': '11',
    'декабря': '12'
}

df['date'] = df['date'].replace(months, regex=True)


df['date'] = pd.to_datetime(df['date'], format='%d %m %Y')

df['date'] = df["date"].dt.strftime('%Y-%m')

df.to_csv('rea_news.csv', index=False)