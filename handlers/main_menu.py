from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import BadRequest

import defines
from db_requests import Links_db
from init import dp
from keyboards.keyboard_builder import build_column_keyboard
from states.user_states import UserStates


@dp.message_handler(filters.CommandStart(), state="*")
async def start(message: types.Message):
    await main_menu(message)


@dp.message_handler(commands=["menu"])
async def main_menu(message: types.Message):
    await main_menu_success(message)


# todo: Динамическая смена пароля
@dp.message_handler(commands=["main_menu_success"])
async def main_menu_success(message: types.Message):
    texts = [defines.START_TRAIN, defines.USER_PROFILE]
    callbacks = ["train_choose_theme", "user_profile"]
    links = [None, None]
    length_without_links = len(texts)
    db_links = await Links_db.get_links()
    for link, text in db_links.items():
        texts.append(text)
        links.append(link)
        callbacks.append(None)
    try:
        await message.answer(defines.GREETING, reply_markup=build_column_keyboard(texts, callbacks, links))
    except BadRequest:
        texts, links, callbacks = texts[:length_without_links], links[:length_without_links], \
                                  callbacks[:length_without_links]
        await message.answer(defines.GREETING, reply_markup=build_column_keyboard(texts, callbacks, links))


@dp.callback_query_handler(text="cancel")
async def _cancel(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    await state.finish()
    callback.message.from_user = callback.from_user
    await main_menu(callback.message)
