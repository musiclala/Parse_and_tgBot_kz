import asyncio
import logging
import json
import requests
from bs4 import BeautifulSoup


# очистка списка объявлений
def clear_cars_list(user_id):
    with open(f'telegram_bots/user_json/cars_dict_{user_id}.json', 'w', encoding='utf-8') as fp:
        print('', file=fp, sep="\n")


# создание нового списка объявлений
def get_first_news(url, user_id):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36"
    }

    cars_dict = {}

    for url_item in url:
        r = requests.get(url=url_item, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")

        list_link = soup.find_all("div", class_="a-elem")

        for i in list_link:
            adt_id = i.find("i").get("data-id")
            title = i.find("span", class_="a-el-info-title").text.strip()
            price = i.find(class_="price").text.split()
            res_price = ' '.join(price)
            detail = i.find(class_="a-search-description").text.strip().split(", ")
            year = f'{detail[0]}'
            capacity = f'{detail[2]} ({detail[3]})'
            city = i.find(class_="list-region").text.strip()
            link = 'https://kolesa.kz' + i.find("a", class_="list-link").get("href")

            cars_dict[adt_id] = {
                "title": title,
                "price": res_price,
                "year": year,
                "capacity": capacity,
                "city": city,
                "link": link,
            }

    with open(f"telegram_bots/user_json/cars_dict_{user_id}.json", "w", encoding="utf-8") as file:
        json.dump(cars_dict, file, indent=4, ensure_ascii=False)


# проверка новых объявлений и добавление в список
def check_cars_update(url, user_id):
    with open(f"telegram_bots/user_json/cars_dict_{user_id}.json", encoding="utf-8") as file:
        cars_list = json.load(file)

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36"
    }

    fresh_cars = {}

    for url_item in url:

        r = requests.get(url=url_item, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")

        list_link = soup.find_all("div", class_="a-elem")

        for i in list_link:
            adt_id = i.find("i").get("data-id")

            if adt_id in cars_list:
                continue
            else:
                title = i.find("span", class_="a-el-info-title").text.strip()
                price = i.find(class_="price").text.split()
                res_price = ' '.join(price)
                detail = i.find(class_="a-search-description").text.strip().split(", ")
                year = f'{detail[0]}'
                capacity = f'{detail[2]} ({detail[3]})'
                city = i.find(class_="list-region").text.strip()
                link = 'https://kolesa.kz' + i.find("a", class_="list-link").get("href")

                cars_list[adt_id] = {
                    "title": title,
                    "price": res_price,
                    "year": year,
                    "capacity": capacity,
                    "city": city,
                    "link": link,
                }

                fresh_cars[adt_id] = {
                    "title": title,
                    "price": res_price,
                    "year": year,
                    "capacity": capacity,
                    "city": city,
                    "link": link
                }

    with open(f"telegram_bots/user_json/cars_dict_{user_id}.json", "w", encoding="utf-8") as file:
        json.dump(cars_list, file, indent=4, ensure_ascii=False)

    return fresh_cars
