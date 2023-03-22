from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from utils import TestStates
import time
from urllib.parse import urlparse
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery
import asyncio
from aiogram.utils import executor
from aiogram.types import ChatActions

TOKEN = '5460899081:AAHrAnMdl69oame0Ah-D7WqB139tO0g7IMI'  # Сюда вы пишите свой токен. Узнать его можно в @BotFather
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
