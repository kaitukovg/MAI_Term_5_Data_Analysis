import requests as rq
from bs4 import BeautifulSoup
from datetime import datetime
import time
import db_functions as db
import pandas as pd

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'Программа заняла: {end - start} секунд')
        return result
    return wrapper

con, cursor = db.connect()

urls = []

for i in range(1, 61):
    page = f"https://www.rea.ru/news?tree-content-path=news&search=&date_from=&date_to=&sub%5B0%5D=57407&page={i}&per-page=12"
    urls.append(page)

@timer
def news_parser(con):
    print('Начинаем парсинг новостей категории "Наука"')
    print("=" * 100)

    data = {
        "title": [],
        "publication_date": [],
        "url": [],
        "detected_at": [],
        "category": []
    }

    for url in urls:
        response = rq.get(url, timeout=10)
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')

        if response.status_code == 200:
            items = soup.select('a.catalog__item-content')

            for item in items:
                title = item.select_one('.catalog__item-title')
                date = item.select_one('.catalog__item-date')
                link = "https://www.rea.ru" + item.get('href')

                data["title"].append(title.get_text(strip=True))
                data["publication_date"].append(date.get_text(strip=True))
                data["url"].append(link)
                data["detected_at"].append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                data["category"].append("science")

        # else:
        #     print(response.status_code)

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

    df['publication_date'] = df['publication_date'].replace(months, regex=True)
    df['publication_date'] = pd.to_datetime(
        df['publication_date'],
        format='%d %m %Y'
    )
    df.to_sql(name='news', con=con, if_exists='append', index=False)

    print('=' * 100)
    print(f'Парсинг закончился, в базу данных сохранено {len(df)} новостей!')

@timer
def check_news():
    print("Проверяем наличие новых новостей...")

    url = "https://www.rea.ru/news?tree-content-path=news&search=&date_from=&date_to=&sub%5B0%5D=57407&page=1&per-page=12"

    response = rq.get(url, timeout=10)

    if response.status_code != 200:
        print(f"Ошибка: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    item = soup.select_one("a.catalog__item-content")

    if not item:
        print("Новости не найдены")
        return

    title = item.select_one(".catalog__item-title")
    date = item.select_one(".catalog__item-date")
    link = "https://www.rea.ru" + item.get("href")

    title_text = title.get_text(strip=True)

    print(f"Последняя новость на сайте: {title_text}")

    result = db.get_last_news(con, cursor)

    if result is None:
        print("База данных пустая")
        db.insert_news(con, cursor, title, date, link)
        return

    last_title = result[0]

    if title_text == last_title:
        print("Новых новостей нет")
        return

    print("Обнаружена новая новость!")

    db.insert_news(con, cursor, title, date, link)

if __name__ == "__main__":
    result = db.get_last_news(con, cursor)

    if result is None:
        print("База данных пустая. Запускаем первоначальный парсинг...")
        news_parser(con)

    else:
        print("База данных уже содержит новости")

    while True:
        check_news()
        time.sleep(300)