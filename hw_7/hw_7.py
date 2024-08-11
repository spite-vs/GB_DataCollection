"""
Скрипт для выявления подписок закрытого аккаунта
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from random import uniform, randint
import csv

target_name = '' # Имя закрытого целевого аккаунта, подписки которого необходимо найти
search_name = '' # Имя первого аккаунта, с которого начинается проверка
base_url = 'https://www.instagram.com/'


user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
options = Options()
options.add_argument(f'user-agent={user_agent}')
driver = webdriver.Chrome(options=options)
driver.get(base_url)

wait = WebDriverWait(driver, 10)
input_name = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='username']")))
input_password = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
time.sleep(uniform(1,3))
input_name.send_keys('') # Вставляем имя аккаунта для входа в соцсеть
time.sleep(uniform(1,3))
input_password.send_keys('') # Вставляем пароль от аккаунта для входа в соцсеть
time.sleep(uniform(1,2))
submit = driver.find_element(By.XPATH, "//button[@type='submit']")
submit.click()

names_not_checked =[search_name]
friends_target = []
closed_account = []
checked_account = []

# Ждём пароль на вход
time.sleep(uniform(30,45)) 


try:
    # Цикл погружения проверки на подписку, с циклом равным 2-ум проверим всех подписчиков известного аккаунта на то, являются ли они подписчиком целевого объекта, если их аккаунт не закрыт
    for i in range(2):
        for search_name in names_not_checked[:20]: # Один аккаунт мне уже заблочили, поэтому проверяем первые 20 подписчиков
            names_lst = []
            user_url = f'https://www.instagram.com/{search_name}/'
            driver.get(user_url)
            
            wait = WebDriverWait(driver, 10)
            count_elements = 0
            time.sleep(uniform(1,2))
            try:
                screen_friends = driver.find_element(By.XPATH, "//a[substring(@href, string-length(@href) - 10) = '/followers/']/span[@title]").get_attribute('title')
                # Допущение, что аккаунты с подписчиками более 1000 являются бизнесовыми
                if int(screen_friends) > 1000:
                    continue
                followers = driver.find_element(By.XPATH, "//a[substring(@href, string-length(@href) - 10) = '/followers/']")
                followers.click()
                time.sleep(uniform(3,4))
                element_to_scroll = driver.find_element(By.XPATH, "//div[@style = 'height: auto; overflow: hidden auto;']/parent::*")
                while True:
                    names = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@role='dialog']/div//a")))
                    if len(names) == count_elements:
                        break    
                    count_elements = len(names)
                    driver.execute_script(f"return arguments[0].scrollBy(0, {randint(1500,1800)});", element_to_scroll)

                    time.sleep(uniform(1,2))
                    if len(names) == count_elements:
                        time.sleep(1)
                    if len(names) == count_elements:
                        time.sleep(4)
                for name in names:
                    el = name.get_attribute('href').split('/')[-2]
                    names_lst.append(el)
                if target_name in names_lst:
                    friends_target.append(search_name)
                    
            except Exception:
                print("Пользователь с закрытой страницей")
                closed_account.append(search_name)
            checked_account.append({
                'account': search_name,
                'screen_friends': screen_friends, 
                'len_parse_friends': len(names_lst)
                })
            
            # Если проверяемый аккаунт является подписчиком целевого объекта, то добавляем список его друзей к списку проверяемых аккаунтов за вычетом дублей и уже проверенных
            if search_name in friends_target:
                names_not_checked = list(set(names_not_checked + names_lst))
            names_not_checked =  list(set(names_not_checked) - set(x['account'] for x in checked_account))
finally:
    driver.quit()

    # Сохраним найденный список подписок целевого объекта, список закрытых аккаунтов, потенциально связанных, которые обнаружили в процессе парсинга и список проверенных на подписку аккаунтов
    with open('friends.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(friends_target)
        
    with open('closed.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(closed_account)
        
    with open('checked.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f,fieldnames=['account','screen_friends', 'len_parse_friends'])
        writer.writeheader()
        writer.writerows(checked_account)