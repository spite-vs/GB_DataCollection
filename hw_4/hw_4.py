# Выберите веб-сайт с табличными данными, который вас интересует.
# Напишите код Python, использующий библиотеку requests для отправки HTTP GET-запроса на сайт и получения HTML-содержимого страницы.
# Выполните парсинг содержимого HTML с помощью библиотеки lxml, чтобы извлечь данные из таблицы.
# Сохраните извлеченные данные в CSV-файл с помощью модуля csv.

# Ваш код должен включать следующее:

# Строку агента пользователя в заголовке HTTP-запроса, чтобы имитировать веб-браузер и избежать блокировки сервером.
# Выражения XPath для выбора элементов данных таблицы и извлечения их содержимого.
# Обработка ошибок для случаев, когда данные не имеют ожидаемого формата.
# Комментарии для объяснения цели и логики кода.

# Примечание: Пожалуйста, не забывайте соблюдать этические и юридические нормы при веб-скреппинге.


from csv import DictWriter
import requests
from lxml import html
import time
from decimal import Decimal


base_url = 'https://finance.yahoo.com/markets/stocks/'

def yahoo_traiding_parse(url: str) -> dict:
    """Функция для парсинга значений из таблицы на сайте finance.yahoo.com с их приведением к соответствующим форматам"""
    counter = 0   
    count = 1
    data = []
    while counter <= count:
        url2 = url + f'?start={counter}&count=250'
        time.sleep(5)
        session = requests.Session()
        response = session.get(url2, headers={
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
'cookie': '', # Здесь были куки, ибо без них работает четвертинка на половинку
'accept-encoding': 'gzip, deflate, br, zstd',
'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}, allow_redirects=True)
        print(response.status_code)
        if 200 <= response.status_code < 300:
            print(f'Паршу страницу {url2}')
            tree = html.fromstring(response.content)
            if tree.xpath("//div[@class = 'total yf-1tdhqb1']/text()"):
                count = int(tree.xpath("//div[@class = 'total yf-1tdhqb1']/text()")[0].split()[-1])
            
            table_rows = tree.xpath("//tbody/tr")
            
            for i, row in enumerate(table_rows):
                try:
                    data.append({
                        "Symbol": row.xpath(".//td[1]/span/div/a/div/span[1]/text()")[0],
                        "Company_name": row.xpath(".//td[1]/span/div/a/div/span[2]/text()")[0],
                        "Price": Decimal(row.xpath(".//td[2]/span/fin-streamer/@data-value")[0].replace(',', '')),
                        "Change_abs": Decimal(row.xpath(".//td[3]/span/fin-streamer/span/text()[1]")[0].replace(',', '').replace('-', '0')
                                            if row.xpath(".//td[3]/span/fin-streamer/span/text()[1]") and row.xpath(".//td[3]/span/fin-streamer/span/text()[1]")[0] !='+'
                                            else row.xpath(".//td[3]/span/fin-streamer/span/text()[2]")[0].replace(',', '').replace('-', '0')
                                            if row.xpath(".//td[3]/span/fin-streamer/span/text()[1]")
                                            else '0'),
                        "Change_rel": Decimal(row.xpath(".//td[4]/span/fin-streamer/span/text()[1]")[0].replace('%', '').replace(',', '').replace('-', '0') 
                                            if row.xpath(".//td[4]/span/fin-streamer/span/text()[1]") and row.xpath(".//td[4]/span/fin-streamer/span/text()[1]")[0] != '+' 
                                            else row.xpath(".//td[4]/span/fin-streamer/span/text()[2]")[0].replace('%', '').replace(',', '').replace('-', '0')
                                            if row.xpath(".//td[4]/span/fin-streamer/span/text()[1]")
                                            else '0')/100,
                        "Volume": Decimal(row.xpath(".//td[5]/span/fin-streamer/text()")[0].replace(',', '')[:-1])*1000000
                                            if row.xpath(".//td[5]/span/fin-streamer/text()")[0][-1] == 'M'
                                            else Decimal(row.xpath(".//td[5]/span/fin-streamer/text()")[0].replace(',', '')[:-1])*1000000000
                                            if row.xpath(".//td[5]/span/fin-streamer/text()")[0][-1] == 'B'
                                            else Decimal(row.xpath(".//td[5]/span/fin-streamer/text()")[0].replace(',', '')),
                        "Avg_vol_3M": Decimal(row.xpath(".//td[6]/span/text()")[0].replace(',', '')[:-1])*1000000
                                            if row.xpath(".//td[6]/span/text()")[0][-1] == 'M'
                                            else Decimal(row.xpath(".//td[6]/span/text()")[0].replace(',', '')[:-1])*1000000000
                                            if row.xpath(".//td[6]/span/text()")[0][-1] == 'B'
                                            else Decimal(row.xpath(".//td[6]/span/text()")[0].replace(',', '')),
                        "Market_cap": '0' if not row.xpath(".//td[7]/span/fin-streamer/text()")
                                            else Decimal(row.xpath(".//td[7]/span/fin-streamer/text()")[0].replace(',', '')[:-1])*1000000
                                            if row.xpath(".//td[7]/span/fin-streamer/text()")[0][-1] == 'M'
                                            else Decimal(row.xpath(".//td[7]/span/fin-streamer/text()")[0].replace(',', '')[:-1])*1000000000
                                            if row.xpath(".//td[7]/span/fin-streamer/text()")[0][-1] == 'B'
                                            else Decimal(row.xpath(".//td[7]/span/fin-streamer/text()")[0].replace(',', '')[:-1])*1000000000000
                                            if row.xpath(".//td[7]/span/fin-streamer/text()")[0][-1] == 'T'
                                            else Decimal(row.xpath(".//td[7]/span/fin-streamer/text()")[0].replace(',', '')),
                        "PE_ratio_TTM": Decimal(row.xpath(".//td[8]/span/text()")[0].replace('-', '0').replace(',', '')),
                        "Wk_change_rel": Decimal(row.xpath(".//td[9]/span/text()")[0].replace('%', ''))/100
                    })
                except Exception:
                    print(f'Что-то не получилось со строкой {i+1}')               
        else:
            print(f'Что-то пошло не так на странице {url}')
        counter +=250
    return data


def write_to_csv(data: list[dict], name: str) -> None:
    """Функция для записи списка словарей в csv"""
    if not data:
        print("Ничего не приехало")
        return
    fieldnames = data[0].keys()
    with open(name + '.csv', 'w', newline='', encoding='utf-8') as f:
        writer = DictWriter(f,fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        

pages = ['trending', 'most-active', 'gainers', 'losers', '52-week-losers', '52-week-gainers']
for page in pages:
    write_to_csv(yahoo_traiding_parse(base_url + page + '/'), page)
