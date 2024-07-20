# Сценарий Foursquare
# Напишите сценарий на языке Python, который предложит пользователю ввести интересующую его категорию (например, кофейни, музеи, парки и т.д.).
# Используйте API Foursquare для поиска заведений в указанной категории.
# Получите название заведения, его адрес и рейтинг для каждого из них.
# Скрипт должен вывести название и адрес и рейтинг каждого заведения в консоль.

import requests
import json

url = "https://api.foursquare.com/v3/places/search"
apikey = 'fsq3nIbYxK1supV4kcCf3K0hs0BKXbvKQXg5IgkpiRjWfe8='


city = input('Город: ')
query = input('Ищем: ')

headers = {"accept": "application/json", "authorization": apikey}
params = {'near': city, 'query': query,'limit': 10}

response = requests.get(url, params=params, headers=headers)

if 200 <= response.status_code < 300:
    data = response.json()
    venues = data["results"]
    result = [{'name': venue['name'], 'address': venue.get('location', {}).get('address', None), 'rating': venue.get('rating', None)} for venue in venues]
    for item in result:
        for key, value in item.items():
            print(f'{key}: {value}')
        print()
else:
    print('Что-то пошло не так')
