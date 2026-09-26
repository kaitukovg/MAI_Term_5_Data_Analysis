import sqlite3 as sql
from datetime import datetime

def connect():
    conn = sql.connect("rea_news.db")
    cursor = conn.cursor()
    return conn, cursor

def create_table(con, cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            publication_date TEXT NOT NULL,
            url TEXT NOT NULL UNIQUE,
            detected_at TEXT NOT NULL,
            category TEXT NOT NULL
        );
    """)

    con.commit()

def insert_news(con, cursor, title, date, link, ):
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

    print("Новые новости загружены")

def view_data(con, cursor):
    s = cursor.execute("SELECT * FROM news")
    print(s.fetchall())

def truncate_table(con, cursor):
    cursor.execute("DELETE FROM news")
    con.commit()

def get_last_news(con, cursor):
    cursor.execute("""
        SELECT title
        FROM news
        ORDER BY id DESC
        LIMIT 1
    """)

    return cursor.fetchone()


if __name__ == "__main__":
    con, cursor = connect()
    view_data(con, cursor)