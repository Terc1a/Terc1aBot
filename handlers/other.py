from aiogram import types, Dispatcher
from create_bot import dp
import json
import string
from keylinks import api_key
import datetime as dt


@dp.message_handler(lambda message: ('cenz.json') in message.text)
async def echo_send(message: types.Message):
    if message.text == 'привет бот':
        await message.reply('И тебе привет :)')
        print('hello bot')
    elif message.text == 'Привет бот':
        await message.reply('И тебе привет :)')
    elif message.text == 'спокойной ночи бот':
        await message.reply('И тебе сладких снов солнышко:*')
    elif message.text == 'Спокойной ночи бот':
        await message.reply('И тебе сладких снов солнышко:*')


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_send)


if __name__ == '__main__':
    executor.start_polling(dp)