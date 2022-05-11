import asyncio
import logging

from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN_KOLESA

import telegram_bots.postgres as postgres
import telegram_bots.functions as functions

# Объект бота
bot = Bot(token=TOKEN_KOLESA, parse_mode=types.ParseMode.HTML)
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# инициализируем соединение с БД
# db = SQLighter('db.db')

time = 1


# Приветствие
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    mess = message.chat.id
    postgres.set_write_message('/start', message.from_user.id)
    await bot.send_message(mess, f"<b>Имя:</b>   {message.from_user.first_name}\n"
                                 f"<b>Имя пользователя:</b>   {message.from_user.username}\n"
                                 f"<b>ID:</b>   {message.from_user.id}\n"
                                 f"<b>Текст:</b>   {message.text}")

    with open(r'photo/welcome.tgs', 'rb') as start_sticker:
        await bot.send_sticker(message.from_user.id, start_sticker)
    await message.answer(f"Привет, <b>{message.from_user.first_name}</b> ! Меня зовут <b>KolesaBot</b>\n\n"
                         f"Я стану твоим помощником в поиске самых свежих объявлений на сайте Kolesa.kz !\n\n"
                         f"Чтобы начать работу давай подберем тариф именно для тебя, а также настроим фильтры! \n\n"
                         f"Перейди в свой личный кабинет по команде: /profile ")


# команда активации бота
@dp.message_handler(commands=['go'])
async def start_bot(message: types.Message):
    url = postgres.get_url_user(message.from_user.id)
    mess = message.chat.id
    postgres.set_write_message('/go', message.from_user.id)
    await bot.send_message(mess, f"<b>Имя:</b>   {message.from_user.first_name}\n"
                                 f"<b>Имя пользователя:</b>   {message.from_user.username}\n"
                                 f"<b>ID:</b>   {message.from_user.id}\n"
                                 f"Нажал кнопку активации ✅")

    if postgres.subscriber_exists(message.from_user.id):
        if not postgres.status_exists(message.from_user.id):
            # если у пользователя не активирован бот, активируем его
            postgres.update_subscription(message.from_user.id, True)
            await message.answer("Бот успешно активирован  ✅")
            functions.get_first_news(url, message.from_user.id)

            while True:
                if postgres.status_exists(message.from_user.id):
                    fresh_adt = functions.check_cars_update(url=url, user_id=message.from_user.id)
                    if len(fresh_adt) > 0:
                        adt = ''
                        for k, v in fresh_adt.items():
                            if k == 'Название':
                                adt += f'<b>{v}</b>\n'
                            elif k == 'Ссылка':
                                adt += f'{v}\n'
                            elif not k:
                                continue
                            else:
                                adt += f'{k}:  {v}\n'

                        await bot.send_message(message.from_user.id, adt, disable_notification=True)
                    await asyncio.sleep(time)
                else:
                    functions.clear_cars_list(message.from_user.id)
                    await asyncio.sleep(time)
        else:
            # если у пользователя уже активирован бот, просто говорим ему об этом
            await message.answer("Бот уже активирован  ⚠")
    else:
        await message.answer("Вы не подписаны на рассылку  ⚠")


# команда остановки бота
@dp.message_handler(commands=['stop'])
async def stop_bot(message: types.Message):
    mess = message.chat.id
    postgres.set_write_message('/stop', message.from_user.id)
    await bot.send_message(mess, f"<b>Имя:</b>   {message.from_user.first_name}\n"
                                 f"<b>Имя пользователя:</b>   {message.from_user.username}\n"
                                 f"<b>ID:</b>   {message.from_user.id}\n"
                                 f"Нажал кнопку деактивации ❌")
    if postgres.subscriber_exists(message.from_user.id):
        if postgres.status_exists(message.from_user.id):
            # если у пользователя активирован бот, отключаем его
            postgres.update_subscription(message.from_user.id, False)
            await message.answer("Бот отключен  ❌")
        else:
            # если у пользователя уже отключен бот, просто говорим ему об этом
            await message.answer("Бот уже отключен  ⚠")
    else:
        await message.answer("Вы не подписаны на рассылку  ⚠")


@dp.message_handler(commands=['restart'])
async def restart_bot(message: types.Message):
    postgres.set_write_message('/restart', message.from_user.id)
    await stop_bot(message)
    await start_bot(message)


# показать user_id
@dp.message_handler(commands=['user_id'])
async def subscribe(message: types.Message):
    mess = message.chat.id
    postgres.set_write_message('/user_id', message.from_user.id)
    await bot.send_message(mess, f"Ваш user id:\n{message.from_user.id}")


# обработка сообщений
# @dp.message_handler()
# async def unsubscribe(message: types.Message):
#     mess = message.chat.id
#     await bot.send_message(mess, f"<b>Имя:</b>   {message.from_user.first_name}\n"
#                                            f"<b>Имя пользователя:</b>   {message.from_user.username}\n"
#                                            f"<b>ID:</b>   {message.from_user.id}\n"
#                                            f"<b>Текст:</b>   {message.text}")
#
#     if message.text.startswith("https://kolesa.kz/cars/"):
#         pass


async def new_adt(time):
    while True:
        postgres.get_subscriptions()
        await asyncio.sleep(time)


# обработка сообщений
@dp.message_handler()
async def unsubscribe(message: types.Message):
    postgres.set_write_message(message.text, message.from_user.id)
    # сюда сделать вывод какой-то, что такой команды нет


# if __name__ == '__main__':
def start_bot_under_dj():
    loop = asyncio.get_event_loop()
    loop.create_task(new_adt(2))
    executor.start_polling(dp, skip_updates=True)
