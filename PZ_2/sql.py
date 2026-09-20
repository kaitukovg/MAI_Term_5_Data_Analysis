import sqlite3 as sql

con = sql.connect("rea_news.db")
cursor = con.cursor()

s = cursor.execute("SELECT * FROM news")
print(s.fetchall())