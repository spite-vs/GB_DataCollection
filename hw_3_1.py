# Установите MongoDB на локальной машине, а также зарегистрируйтесь в онлайн-сервисе. https://www.mongodb.com/ https://www.mongodb.com/products/compass
# Загрузите данные который вы получили на предыдущем уроке путем скрейпинга сайта с помощью Buautiful Soup 
# в MongoDB и создайте базу данных и коллекции для их хранения.


import json
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['hw']
collection = db['books']

with open('hw_2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

collection.insert_many(data)