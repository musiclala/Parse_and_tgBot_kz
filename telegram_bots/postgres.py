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
    result = open()
    result.execute(f"select list_url from posting_client WHERE user_id = '{user_id}'")
    conn.commit()
    close()
    if type(result.fetchall()) == 'list':
        return result.fetchall()[0][0].split(', ')
    else:
        return result.fetchall()


def set_write_message(text_mess, user_id):
    result = open()
    result.execute(f"INSERT INTO posting_messagelog(created_mess, log_text, mess_log_user_id) "
                   f"VALUES ('{timezone.now()}', '{text_mess}',{user_id})")
    conn.commit()
    close()
    return result



