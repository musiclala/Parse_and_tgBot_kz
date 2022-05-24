import json

import psycopg2.errors
import requests
from bs4 import BeautifulSoup
import telegram_bots.postgres as postgres

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36"
}


def check_json_data(item, key_value):
    try:
        variable = item[key_value]
    except KeyError:
        variable = ''
    return variable


def find_regions_and_cities():
    r = requests.get(url='https://m.kolesa.kz/car/brands/?category=auto.car', headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    json_region_and_city = json.loads(soup.find("p").text)

    for item_region_or_city in json_region_and_city:

        value = check_json_data(item_region_or_city, 'value')
        alias_city = check_json_data(item_region_or_city, 'alias')
        parent = check_json_data(item_region_or_city, 'parent')
        isKz = check_json_data(item_region_or_city, 'isKz')
        kz = check_json_data(item_region_or_city, 'kz')

        if isKz:
            try:
                postgres.add_region_to_kolesa(value, alias_city)
            except (psycopg2.errors.UniqueViolation, psycopg2.errors.InFailedSqlTransaction):
                pass

        if kz:
            try:
                postgres.add_city_to_kolesa(value, alias_city, parent)
            except (psycopg2.errors.UniqueViolation, psycopg2.errors.InFailedSqlTransaction):
                pass


def find_brands_and_models():
    r = requests.get(url='https://m.kolesa.kz/car/brands/?category=auto.car', headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    json_brand = json.loads(soup.find("p").text)

    for item_brand in json_brand:

        id_brand = check_json_data(item_brand, 'id')
        value_brand = check_json_data(item_brand, 'value')
        name_brand = check_json_data(item_brand, 'name')

        try:
            postgres.add_brand_to_kolesa(value_brand, name_brand)
        except (psycopg2.errors.UniqueViolation, psycopg2.errors.InFailedSqlTransaction):
            pass

        r = requests.get(url=f'https://m.kolesa.kz/car/models/{id_brand}/', headers=headers)
        soup = BeautifulSoup(r.text, "lxml")
        json_model = json.loads(soup.find("p").text)

        for item_model in json_model:
            value_model = check_json_data(item_model, 'value').replace('\'', '-')
            name_model = check_json_data(item_model, 'name')

            try:
                postgres.add_model_to_kolesa(value_model, name_model, value_brand)
            except (psycopg2.errors.UniqueViolation, psycopg2.errors.InFailedSqlTransaction):
                pass


def find_other_data():
    r = requests.get(url='https://m.kolesa.kz/constructor/search/2/', headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    json_other_data = json.loads(soup.find("p").text)
    for item_data in json_other_data['fields']:

        label_data = check_json_data(item_data, 'label')
        name_url_data = check_json_data(item_data, 'name')
        component_data = check_json_data(item_data, 'component')
        options_data = check_json_data(item_data, 'options')

        postgres.add_other_filtres_to_kolesa(label_data, name_url_data, component_data, str(options_data).replace('\'', '"'))


if __name__ == '__main__':
    find_regions_and_cities()
    find_brands_and_models()
    find_other_data()
