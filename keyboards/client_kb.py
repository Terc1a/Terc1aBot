from re import T
from aiogram import Dispatcher, types
from create_bot import dp, bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.utils import executor

b1 = KeyboardButton('/Начать')
b2 = KeyboardButton('/Помощь')
b3 = KeyboardButton('/Меню')
b4 = KeyboardButton('Отправить где я', request_location=True)
b5 = KeyboardButton('Поделиться номером', request_contact=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_client.add(b1).insert(b2).add(b3).insert(b4).add(b5)

def register_handlers_ckb(dp: Dispatcher):

