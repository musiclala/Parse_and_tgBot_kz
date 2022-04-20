import json
import requests
from bs4 import BeautifulSoup


def clear_cars_list(file_name):
    with open(file_name, 'w', encoding='utf-8') as fp:
        print('', file=fp, sep="\n")


def get_first_news(urls):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36"
    }

    url = urls
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")

    list_link = soup.find_all("div", class_="a-elem")

    cars_dict = {}
    for i in list_link:

        user_id = i.find("i").get("data-id")
        title = i.find("span", class_="a-el-info-title").text.strip()
        price = i.find(class_="price").text.split()
        res_price = ' '.join(price)
        detail = i.find(class_="a-search-description").text.strip().split(", ")
        year = f'{detail[0]}'
        capacity = f'{detail[2]} ({detail[3]})'
        city = i.find(class_="list-region").text.strip()
        link = 'https://kolesa.kz' + i.find("a", class_="list-link").get("href")

        cars_dict[user_id] = {
            "title": title,
            "price": res_price,
            "year": year,
            "capacity": capacity,
            "city": city,
            "link": link,
        }

    with open("cars_dict.json", "w", encoding="utf-8") as file:
        json.dump(cars_dict, file, indent=4, ensure_ascii=False)


def check_cars_update(urls):
    with open("cars_dict.json", encoding="utf-8") as file:
        cars_list = json.load(file)

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36"
    }

    url = urls
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")

    list_link = soup.find_all("div", class_="a-elem")

    fresh_cars = {}
    for i in list_link:
        user_id = i.find("i").get("data-id")

        if user_id in cars_list:
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

            cars_list[user_id] = {
                "title": title,
                "price": res_price,
                "year": year,
                "capacity": capacity,
                "city": city,
                "link": link,
            }

            fresh_cars[user_id] = {
                "title": title,
                "price": res_price,
                "year": year,
                "capacity": capacity,
                "city": city,
                "link": link
            }

    with open("cars_dict.json", "w", encoding="utf-8") as file:
        json.dump(cars_list, file, indent=4, ensure_ascii=False)

    return fresh_cars


def main():
    check_cars_update()


if __name__ == "__main__":
    main()
