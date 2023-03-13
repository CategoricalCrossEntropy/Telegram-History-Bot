from aiogram import types

import defines
from database import sqlite_db
from init import dp
from keyboards.keyboard_builder import build_column_keyboard


@dp.message_handler(commands=["start"], state="*")
async def start(message: types.Message):
    await main_menu(message)


@dp.message_handler(commands=["menu"])
async def main_menu(message: types.Message):
    texts = [defines.START_TRAIN_9, defines.START_TRAIN_10]
    callbacks = ["train_9", "train_10"]
    links = [None, None]
    db_links = await sqlite_db.get_links()
    for link, text in db_links.items():
        texts.append(text)
        links.append(link)
        callbacks.append(None)
    await message.answer(defines.GREETING, reply_markup=build_column_keyboard(texts, callbacks, links))
