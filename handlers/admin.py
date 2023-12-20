from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, \
    InlineKeyboardButton

from create_bot import dp, bot
from data_base import sqlite_db
from keyboards import admin_kb
from keylinks import *

ID = None


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()


# Получаем id админа
@dp.message_handler(commands=['m'], is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, welcome,
                           reply_markup=admin_kb.button_case_admin)
    await message.delete()


# Начало диалога загрузки нового пункта меню


async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Загрузи мем')

    # Выход из состояний


async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('OK')


# Ловим ответ и пишем в словарь


async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.reply('Теперь напиши номерочек мема')


# Ловим второй ответ


async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Теперь добавь анекдот с:')


# Ловим последний ответ


async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text

    async with state.proxy() as data:
        await message.reply(str(data))

    await sqlite_db.sql_add_command(state)
    await state.finish()


# Удаление записи
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace("del ", ""))
    await callback_query.answer(text=f'запись удалена', show_alert=True)


@dp.message_handler(commands='Удалить')
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]} {ret[2]}')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup(). \
                                   add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))
            return delete_item


@dp.message_handler(commands='полезное')
async def url_command(message: types.Message):
    await message.answer('Ссылочки', reply_markup=urlkb)


urlkb = InlineKeyboardMarkup(row_width=2)
url_btn_motivation = InlineKeyboardButton(text='Мотивашки',
                                          url='https://youtube.com/playlist?list=PLAzRZ-VSmW56gBWgLALm8JjagUXewvE3m')
url_btn_mygroup = InlineKeyboardButton(text='Моя группа вк', url='https://vk.com/terceverything')
urlkb.add(url_btn_motivation, url_btn_mygroup)


# Регистрируем хендлеры
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(cancel_handler, commands='отмена', state="*")
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(make_changes_command, commands=['m'], is_chat_admin=True)
    dp.register_message_handler(url_command, commands=['полезное'])
