import datetime

import psycopg2
import config
from django.utils import timezone

conn = psycopg2.connect(dbname=config.NAME_DB, user=config.USERID_DB,
                        password=config.PASS_DB, host=config.HOST_DB, port=config.PORT_DB)


def open():
    """Подключаемся к БД и сохраняем курсор соединения"""
    cursor = conn.cursor()
    return cursor


def close():
    """Закрываем соединение с БД"""
    open().close()


def get_subscriptions(status=True):
    """Получаем всех активных подписчиков бота"""
    result = open()
    result.execute(f"SELECT * FROM posting_client WHERE status_bot = {status};")
    close()
    return result.fetchall()


def subscriber_exists(user_id):
    """Проверяем есть ли уже user в базе"""
    result = open()
    result.execute(f"SELECT * FROM posting_client WHERE user_id = '{user_id}';")
    close()
    return bool(len(result.fetchall()))


def status_exists(user_id):
    """Проверяем статус пользователя"""
    result = open()
    result.execute(f"SELECT * FROM posting_client WHERE user_id = {user_id} and status_bot = 'True';")
    close()
    return bool(len(result.fetchall()))


def add_subscriber(user_id, status_bot):
    """Добавляем нового подписчика"""
    result = open()
    result.execute(f"INSERT INTO posting_client VALUES ({user_id}, {False})")
    conn.commit()
    close()
    return result


def update_subscription(user_id, status):
    """Обновляем статус подписки"""
    result = open()
    result.execute(f"UPDATE posting_client SET status_bot = '{status}' WHERE user_id = '{user_id}'")
    conn.commit()
    close()
    return result


def get_url_user(user_id):
    """Получаем список ссылок пользователя"""
    result = open()
    result.execute(f"select list_url from posting_client WHERE user_id = '{user_id}'")
    conn.commit()
    close()
    if type(result.fetchall()) == 'list':
        return result.fetchall()[0][0].split(', ')
    else:
        return result.fetchall()


def set_write_message(text_mess, user_id):
    """Записываем любые сообщения в боте"""
    result = open()
    result.execute(f"INSERT INTO posting_messagelog(created_mess, log_text, mess_log_user_id) "
                   f"VALUES ('{timezone.now()}', '{text_mess}',{user_id})")
    conn.commit()
    close()
    return result


def add_region_to_kolesa(name_region, alias_region):
    """Проверяем, есть ли регион в базе, если нет, то добавляем"""
    result = open()

    result.execute(f"select * from posting_regionfilters where alias_region = '{alias_region}'")
    if bool(len(result.fetchall())):
        close()
        return True
    else:
        result.execute(f'insert into posting_regionfilters(name_region, alias_region)'
                       f"values ('{name_region}', '{alias_region}')")
        conn.commit()
        close()
        return result


def add_city_to_kolesa(name_city, alias_city, parent_city):
    """Проверяем, есть ли город в базе, если нет, то добавляем"""
    result = open()
    result.execute(f"select * from posting_cityfilters where alias_city = '{alias_city}'")
    if bool(len(result.fetchall())):
        close()
        return True
    else:
        result.execute(f'insert into posting_cityfilters(name_city, alias_city, parent_city_id)'
                       f"values ('{name_city}', '{alias_city}', '{parent_city}')")
        conn.commit()
        close()
        return result


def add_brand_to_kolesa(name_brand, alias_brand):
    """Проверяем, есть ли брэнд в базе, если нет, то добавляем"""
    result = open()

    result.execute(f"select * from posting_brandfilters where alias_brand = '{alias_brand}'")
    if bool(len(result.fetchall())):
        close()
        return True
    else:
        result.execute(f'insert into posting_brandfilters(name_brand, alias_brand)'
                       f"values ('{name_brand}', '{alias_brand}')")
        conn.commit()
        close()
        return result


def add_model_to_kolesa(name_model, alias_model, parent_model):
    """Проверяем, есть ли модель в базе, если нет, то добавляем"""
    result = open()
    result.execute(f"select * from posting_modelfilters where alias_model = '{alias_model}'")
    if bool(len(result.fetchall())):
        close()
        return True
    else:
        result.execute(f'insert into posting_modelfilters(name_model, alias_model, parent_model_id)'
                       f"values ('{name_model}', '{alias_model}', '{parent_model}')")
        conn.commit()
        close()
        return result


def add_other_filtres_to_kolesa(name_data, alias_data, component_data, options_data):
    """Проверяем, есть ли другие фильтры в базе, если нет, то добавляем"""
    result = open()
    result.execute(f"select * from posting_otherdatafilters where alias_data = '{alias_data}'")
    if bool(len(result.fetchall())):
        close()
        return True
    else:
        result.execute(f'insert into posting_otherdatafilters(name_data, alias_data, component_data, options_data)'
                       f"values ('{name_data}', '{alias_data}', '{component_data}', '{options_data}')")
        conn.commit()
        close()
        return result
