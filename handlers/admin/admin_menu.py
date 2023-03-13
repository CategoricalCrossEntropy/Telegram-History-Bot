from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import config
import defines
from database import sqlite_db
from init import dp
from keyboards.keyboard_builder import build_column_keyboard
from states.admin_states import EditStates
from handlers.main_menu import main_menu


@dp.message_handler(commands=["edit"])
async def edit(message: types.Message):
    admin_ids = await sqlite_db.get_admins()
    await EditStates.password_request.set()
    if str(message.from_user.id) in admin_ids:
        await EditStates.password_success.set()
        await admin_menu(message)
        return
    await message.answer(defines.PASSWORD_REQUEST)


@dp.message_handler(Text(equals=config.PASSWORD), state=EditStates.password_request)
async def admin_success_auth(message: types.Message):
    await sqlite_db.add_admin(message.from_user.id)
    await message.answer("Успешная авторизация!")
    await admin_menu(message)


@dp.message_handler(state=EditStates.password_request)
async def admin_failed_auth(message: types.Message):
    await message.answer("Неверный пароль для авторизации. Попробуйте ещё раз.")


@dp.message_handler(state=EditStates.password_success)
async def admin_menu(message: types.Message):
    await EditStates.password_success.set()
    answers = [defines.ADMIN_MENU_SHOW, defines.ADMIN_MENU_ADD,
               defines.ADMIN_MENU_DELETE, defines.ADMIN_MENU_MULTI_ADD,
               defines.ADMIN_MENU_LINKS_EDIT, defines.CANCEL_COMMAND]
    callback = ["show_questions", "add_question",
                "delete_question", "add_several_questions",
                "edit_links", "cancel"]
    await message.answer(defines.ADMIN_MENU_TEXT,
                         reply_markup=build_column_keyboard(answers, callback))


@dp.callback_query_handler(text="cancel", state="*")
async def back_to_menu(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    await state.finish()
    callback.message.from_user = callback.from_user
    await main_menu(callback.message)


@dp.callback_query_handler(text="admin_cancel", state="*")
async def back_to_admin_menu(callback: types.CallbackQuery):
    await callback.message.delete_reply_markup()
    await admin_menu(callback.message)
