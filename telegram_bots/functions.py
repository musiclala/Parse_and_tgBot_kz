import asyncio
import logging
import json
import requests
from bs4 import BeautifulSoup


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36"
}


# очистка списка объявлений
def clear_cars_list(user_id):
    with open(f'telegram_bots/user_json/cars_dict_{user_id}.json', 'w', encoding='utf-8') as fp:
        print('', file=fp, sep="\n")


# создание нового списка объявлений
def get_first_news(url, user_id):
    cars_dict = {}

    for url_item in url:
        r = requests.get(url=url_item, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")

        list_link = soup.find_all("div", class_="a-elem")

        for i in list_link:
            adt_id = i.find("i").get("data-id")

            cars_dict[adt_id] = {}

    with open(f"telegram_bots/user_json/cars_dict_{user_id}.json", "w", encoding="utf-8") as file:
        json.dump(cars_dict, file, indent=4, ensure_ascii=False)


# проверка новых объявлений и добавление в список
def check_cars_update(url, user_id):
    with open(f"telegram_bots/user_json/cars_dict_{user_id}.json", encoding="utf-8") as file:
        cars_list = json.load(file)

    fresh_cars = {}

    for url_item in url:

        r = requests.get(url=url_item, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")

        list_link = soup.find_all("div", class_="a-elem")

        for i in list_link:
            adt_id = i.find("i").get("data-id")

            if adt_id not in cars_list:
                cars_list[adt_id] = {}

                url_detail = f'https://kolesa.kz/a/show/{adt_id}'
                r = requests.get(url=url_detail, headers=headers)
                soup_detail = BeautifulSoup(r.text, "lxml")

                # Имя объявления
                title_soup = soup_detail.find('h1', class_='offer__title').text.split()
                fresh_cars['Название'] = ' '.join(title_soup)

                # Цена
                price = soup_detail.find(class_="offer__price").text.split()
                fresh_cars['Цена'] = ' '.join(price)

                # Все остальные детали
                detail_link = soup_detail.find_all("dl")
                for i in detail_link:
                    key = i.find('dt', class_='value-title').get('title')
                    value = i.find('dd', class_='value').text.strip()
                    fresh_cars[key] = value

                # Ссылка на объявление
                fresh_cars['Ссылка'] = url_detail
            else:
                continue

    with open(f"telegram_bots/user_json/cars_dict_{user_id}.json", "w", encoding="utf-8") as file:
        json.dump(cars_list, file, indent=4, ensure_ascii=False)

    return fresh_cars
