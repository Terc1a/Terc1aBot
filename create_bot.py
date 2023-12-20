from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keylinks import *

storage = MemoryStorage()

bot = Bot(token=token_key)
dp = Dispatcher(bot, storage=storage)
