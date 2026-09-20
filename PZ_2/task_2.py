import requests as rq
from bs4 import BeautifulSoup
import sqlite3 as sql
from datetime import datetime
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(end - start)
        return result
    return wrapper

@timer
def check_news():
    url = "https://www.rea.ru/news?tree-content-path=news&search=&date_from=&date_to=&sub%5B0%5D=57407&page=2&per-page=12"
    response = rq.get(url)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    if response:
        title = soup.find('div', class_='catalog__item-title')
        date = soup.find('div', 'catalog__item-date')
        link = "https://www.rea.ru" + title.parent.get('href')

    else:
        print(f"Error: {response.status_code}")

    con = sql.connect("rea_news.db")
    cursor = con.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO news(title, publication_date, url, detected_at, category)
        VALUES(?, ?, ?, ?, ?)
    """, (
        title.text.strip(),
        date.text.strip(),
        link,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "science"
    ))

    if cursor.rowcount == 1:
        print("Detected fresh new!")
        print(title.text.strip())
    else:
        print("There is no fresh news!")

    con.commit()
    con.close()

while True:
    check_news()
    time.sleep(300)