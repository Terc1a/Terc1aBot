from os import link
import aiogram
from aiogram import types, executor
from create_bot import dp
from data_base import sqlite_db
import hashlib
import requests
from pprint import pprint
import logging
import youtube_search as ys
import pyrogram
from pyrogram import Client
from keylinks import *
async def on_startup(_):
    print(online)
    sqlite_db.sql_start()



from handlers import client, admin, other
from keyboards import client_kb

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
client_kb.register_handlers_ckb(dp)
other.register_handlers_other(dp)


def searcher(text):
    res = ys.YoutubeSearch(text, max_results=10).to_dict()
    return res


@dp.inline_handler()
async def inline_handler(query: types.InlineQuery):
    text = query.query or 'echo'
    links = searcher(text)

    articles = [types.InlineQueryResultArticle(
        id=hashlib.md5(f'{link["id"]}'.encode()).hexdigest(),
        title=f'{link["title"]}',
        url=f'https://www.youtube.com/watch?v={link["id"]}',
        thumb_url=f'{link["thumbnails"][0]}',
        input_message_content=types.InputTextMessageContent(
            message_text=f'https://www.youtube.com/watch?v={link["id"]}')
    ) for link in links]
    await query.answer(articles, cache_time=60, is_personal=True)

logging.basicConfig(level=logging.INFO, filename="py_bot_log.log",filemode="w")
logging.debug(debug)
logging.info(info)
logging.warning(warning)
logging.error(error)
logging.critical(critical_error)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

