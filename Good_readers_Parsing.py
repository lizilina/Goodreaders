import requests
from bs4 import BeautifulSoup
import sqlite3
import random
import time

url = 'https://www.goodreads.com/list/show/26495.Best_Woman_Authored_Books?page={}'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
response = requests.get(url, headers=headers)

db_name = 'goodreaders_books.db'
conn = sqlite3.connect(db_name)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, author TEXT)''')

for i in range (1,6):
    url = url.format(i)
    print(f"Page {i}...")

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    books_soup = soup.find_all('tr', {'itemtype': 'http://schema.org/Book'})
    for item in books_soup:
        title = item.find('a', {'class': 'bookTitle'}).get_text(strip=True)
        author = item.find('a', {'class': 'authorName'}).get_text(strip=True)
        c.execute('INSERT INTO books (title, author) VALUES (?, ?)', (title, author))
    conn.commit()


    time.sleep(random.randint(10,20))

conn.close()


