# Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/ и извлечь информацию о всех книгах на сайте во всех категориях: 
# название, цену, количество товара в наличии (In stock (19 available)) в формате integer, описание.

# Затем сохранить эту информацию в JSON-файле.

import requests
import json
from bs4 import BeautifulSoup
import urllib.parse
import re

counter = 1
books = []
values_num = 1

while True:
    response = requests.get(f'https://books.toscrape.com/catalogue/page-{counter}.html')
    if  response.status_code < 200 or response.status_code >= 300:
        break
    
    soup = BeautifulSoup(response.content, 'html.parser')
    containers = soup.find_all('article', ('class', 'product_pod'))
    for container in containers:
        book = {}
        book['name'] = container.find('h3').find('a').get('title', '')
        book['price'] = float(container.find('p', ('class', 'price_color')).text.strip()[1:])
        
        rel_link_book = container.find('h3').find('a').get('href')
        link_book = urllib.parse.urljoin('https://books.toscrape.com/catalogue/', rel_link_book)
        response_book = requests.get(link_book)
        soup_book = BeautifulSoup(response_book.content, 'html.parser')
        
        try:
            book['quantity'] = int(re.search(r'(\d+)', soup_book.find('div', ('class', 'col-sm-6 product_main')).find('p', ('class', 'instock availability')).text).group())
        except:
            book['quantity'] = None
        try:
            book['description'] = soup_book.find('div', {'id': 'product_description'}).find_next('p').text
        except:
            book['description'] = None
        books.append(book)
        print(values_num)
        values_num +=1
    counter +=1

    
with open('hw_2.json', 'w') as f:
    json.dump(books, f)
