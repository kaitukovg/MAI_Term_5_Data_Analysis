import sqlite3 as sql
from datetime import datetime

def connect():
    conn = sql.connect("news.db")
    cursor = conn.cursor()

    return conn, cursor

def connect_users():
    conn = sql.connect("users.db")
    cursor = conn.cursor()

    return conn, cursor

def table_news(con, cursor):
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                link TEXT UNIQUE NOT NULL,
                publication_date TEXT NOT NULL,
                category TEXT,
                university TEXT NOT NULL,
                added_at TEXT DEFAULT (datetime('now')),
                content TEXT DEFAULT 'no text'
        );
    """)

    con.commit()

def table_categories(con, cursor):
    print("Создаем таблицу категорий...")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news_categories(
            category_id INTEGER NOT NULL,
            name TEXT NOT NULL
        );
    """)

    count = cursor.execute("""SELECT COUNT(*) FROM news_categories;""").fetchone()[0]

    if count == 0:
        print("Таблица с категориями пустая!\nЗаполняем ее данными...")

        cursor.execute("""
            INSERT INTO news_categories(category_id, name)
                VALUES
                    (1, "Наука"),
                    (2, "Спорт"),
                    (3, "Абитуриентам"),
                    (4, "Объявления"),
                    (5, "Студенчество"),
                    (6, "Международная деятельность"),
                    (7, "Сотрудничество"),
                    (8, "Культура"),
                    (9, "Образование"),
                    (10, "unknown");
        """)

        print(f"Таблица категорий заполнена!")
    else:
        print(f"Таблица категорий заполнена!")

    con.commit()

def table_university(con, cursor):
    print("Создаем таблицу университетов...")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS universities(
            university_id INTEGER NOT NULL,
            name TEXT NOT NULL
        );
    """)
    count = cursor.execute("""SELECT COUNT(*) FROM universities;""").fetchone()[0]

    if count == 0:
        print("Таблица с университетами пустая!\nЗаполняем ее данными...")

        cursor.execute("""
                INSERT INTO universities(university_id, name)
                    VALUES
                        (1, "РЭУ"),
                        (2, "МИРЭА"),
                        (3, "ВШЭ"),
                        (4, "МИСИС"),
                        (5, "МФТИ"),
                        (6, "МАИ"),
                        (7, "КФУ"),
                        (8, "МГУ"),
                        (9, "unknown");
            """)

        print(f"Таблица университетов заполнена!")
    else:
        print(f"Таблица университетов заполнена!")

    con.commit()

def table_users(con, cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT
        );
    """)
    con.commit()

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_categories (
                user_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
        """)
    con.commit()


def insert_news(con, cursor, title, date, link, category, university, content):
    cursor.execute("""
            INSERT OR IGNORE INTO news(title, publication_date, link, added_at, category, university, content)
            VALUES(?, ?, ?, ?, ?, ?, ?)
        """, (
        title.text.strip(),
        date.text.strip(),
        link,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        category,
        university,
        content
    ))

    if cursor.rowcount == 1:
        print("Detected fresh new!")
        print(title.text.strip())
    else:
        print("There is no fresh news!")

    con.commit()

    print("Новые новости загружены")

def view_data(cursor):
    data = cursor.execute("SELECT * FROM news")
    row_count = cursor.execute("SELECT COUNT(*) FROM news").fetchone()[0]

    return data, row_count

def truncate_table(con, cursor):
    cursor.execute("DELETE FROM news")
    con.commit()

def get_last_news(cursor):
    cursor.execute("""
        SELECT title
        FROM news
        ORDER BY publication_date DESC, id DESC
        LIMIT 1
    """)

    return cursor.fetchone()

def truncate(con, cursor, table_name):
    cursor.execute("DELETE FROM ?", (table_name,))
    con.commit()
    print(f"Таблица {table_name} очищена")

if __name__ == "__main__":
    con_n, cursor_n = connect()
    # table_news(con_n, cursor_n)
    # table_categories(con_n, cursor_n)
    # table_university(con_n, cursor_n)
    #
    # a, b = view_data(cursor_n)
    #
    # print(b)

    truncate_table(con_n, cursor_n)