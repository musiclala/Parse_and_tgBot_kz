import asyncio
import logging

from aiogram import Bot, Dispatcher, executor, types

from config import ADMIN_TOKEN
import postgres

# Объект бота
bot = Bot(token=ADMIN_TOKEN, parse_mode=types.ParseMode.HTML)
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# инициализируем соединение с БД
# db = SQLighter('db.db')


# conn = psycopg2.connect(dbname=config.NAME_DB, user=config.USERID_DB,
#                         password=config.PASS_DB, host=config.HOST_DB)
# cursor = conn.cursor()
# cursor.execute('SELECT * FROM client LIMIT 10')
#
# for row in cursor:
#     print(row)
#
# cursor.close()
# conn.close()



@dp.message_handler()
async def start(message: types.Message):
    len_message = message.text.split(', ')
    if len_message[0] == 'add':
        if len(len_message) == 2:
            if not postgres.subscriber_exists(len_message[1]):
                # если юзера нет в базе данных, тогда добавляем его
                postgres.add_subscriber(len_message[1], False)

                await message.answer(f"Пользователь {len_message[1]} добавлен в базу данных   ✅")

            else:
                # если он уже там есть, то просто обновляем ему статус подписки
                postgres.update_subscription(len_message[1], True)
                await message.answer("Пользователь и так уже находится в базе данных   ⚠")
        else:
            await message.answer("Неверный ввод данных ⚠")

    elif len_message[0] == 'info':
        if len(len_message) == 2:
            if postgres.subscriber_exists(len_message[1]):
                # если юзер в базе, проверяем статус активации бота
                await message.answer(f"Статус активации бота {len_message[1]}:   {postgres.status_exists(len_message[1])}")
            else:
                # если пользователя нет в базе данных, отправляем сообщение
                await message.answer("Пользователя нет в базе данных  ❌")
        else:
            await message.answer("Неверный ввод данных ⚠")


async def reload_SQL(time):
    while True:
        postgres.get_subscriptions()
        await asyncio.sleep(time)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(reload_SQL(2))
    executor.start_polling(dp, skip_updates=True)