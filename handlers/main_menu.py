from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from aiogram.utils.exceptions import BadRequest

import defines
from db_requests import Links_db, Codeword_db, Users_db, Admins_db
from init import dp
from keyboards.keyboard_builder import build_column_keyboard
from states.user_states import UserStates


@dp.message_handler(filters.CommandStart(), state="*")
async def start(message: types.Message):
    await main_menu(message)


@dp.message_handler(commands=["menu"])
async def main_menu(message: types.Message):
    user_is_registered = await Users_db.user_is_registered(message.from_user.id)
    codeword_not_specified = await Codeword_db.codeword_is_empty()
    user_is_admin = str(message.from_user.id) in await Admins_db.get_admins()
    if any((user_is_registered, codeword_not_specified, user_is_admin)):
        await main_menu_success(message)
        return
    await UserStates.password_request.set()
    await message.answer(defines.PASSWORD_REQUEST_USER)


@dp.message_handler(state=UserStates.password_request)
async def user_attempt_auth(message: types.Message, state: FSMContext):
    if message.text == await Codeword_db.get_codeword():
        await message.answer("Успешная авторизация!")
        await Users_db.register_user(message.from_user.id)
        await main_menu_success(message)
        await state.finish()
    else:
        await message.answer("Неверный пароль для авторизации. Попробуйте ещё раз:")


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
