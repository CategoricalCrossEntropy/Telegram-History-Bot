from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config


if config.TEST:
    bot = Bot(token=config.TEST_TOKEN)
else:
    bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
