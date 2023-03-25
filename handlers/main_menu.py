from aiogram import types
from aiogram.dispatcher import filters, FSMContext

import defines
from database import sqlite_db
from init import dp
from keyboards.keyboard_builder import build_column_keyboard


@dp.message_handler(filters.CommandStart(), state="*")
async def start(message: types.Message):
    await main_menu(message)


@dp.message_handler(commands=["menu"])
async def main_menu(message: types.Message):
    texts = [defines.START_TRAIN, defines.USER_PROFILE]
    callbacks = ["train_choose_theme", "user_profile"]
    links = [None, None]
    db_links = await sqlite_db.get_links()
    for link, text in db_links.items():
        texts.append(text)
        links.append(link)
        callbacks.append(None)
    await message.answer(defines.GREETING, reply_markup=build_column_keyboard(texts, callbacks, links))


@dp.callback_query_handler(text="cancel")
async def _cancel(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    await state.finish()
    await main_menu(callback.message)
