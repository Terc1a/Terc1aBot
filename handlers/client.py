from aiogram import Dispatcher, types
from create_bot import dp
from create_bot import bot
from keyboards import kb_client
from data_base import sqlite_db
from pprint import pprint
import logging
import requests
from handlers.pyrotest import get_chat_members
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keylinks import *


async def weather_command(message: types.Message):
    city_from_message = message.text[3:]
    city = city_from_message
    api_key = '8c81a12f6d3df42160c575241bf74f03'
    r = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    )
    data = r.json()
    weather1 = data["main"]["temp"]
    weather = round(weather1)
    feels_like1 = data["main"]["feels_like"]
    feels_like = round(feels_like1)
    humidity = data["main"]["humidity"]
    wind_speed1 = data["wind"]["speed"]
    wind_speed = round(wind_speed1)
    print(data)
    
    description = data["weather"][0]["main"]
    # Словарь с соответствием погодных условий и смайликов


    for key in weather_translate:
        if key in description:
            trans = weather_translate[key]
            print(f"Перевод: {trans}")


    for key in weather_emojis:
        if key in description:
            emoji = weather_emojis[key]
            print(f"Состояние погоды: {emoji}")
    try:
        await message.reply(
            f"{trans}{emoji}\nТемпература воздуха: {weather}°C. Ощущается как {feels_like}°C\nСила ветра: {wind_speed}м/с\nВлажность:{humidity}%\n")
        logging.basicConfig(level=logging.INFO, filename="py_message.log", filemode="w")
        logging.info(f"{message.text}")
    except:
        logging.basicConfig(level=logging.INFO, filename="py_message.log", filemode="w")
        logging.info(f"{message.text}")


async def process_message(message: types.Message):
    with open("users.txt") as file:
        usernames = file.read()
        print(usernames)
    await message.reply(usernames)


async def command_bonk(message: types.Message):
    try:
        test = message.reply_to_message
        test2 = message.reply_to_message.from_user.username
        print(test, 'test')
        print(test2, 'test2')
        await message.reply(f'@{test2}, булочка, не надо писать всякие гадости *bonk*')
        await message.delete()
    except:
        print('error bonk')


async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Добро пожаловать в квиз-бота,\n'
                                                     'по кнопкам ниже вы можете ознакомиться с правилами, лицензионным соглашением и сделать первый взнос',
                               reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему:\nhttps://t.me/Terc1aBot')


async def command_start_work(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Здарова заебал', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему:\nhttps://t.me/Terc1aBot')


async def command_help(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Сам себе помоги', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему:\nhttps://t.me/Terc1aBot')


async def bot_menu_command(message: types.Message):
    await sqlite_db.sql_read(message)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(weather_command, commands=['w'])
    dp.register_message_handler(command_start_work, commands=['Начать'])
    dp.register_message_handler(command_help, commands=['Помощь'])
    dp.register_message_handler(bot_menu_command, commands=['Меню'])
    dp.register_message_handler(process_message, commands=['ping'])
    dp.register_message_handler(command_bonk, commands=['bonk'])


if __name__ == '__main__':
    executor.start_polling(dp)
