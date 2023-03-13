from aiogram import types

import defines
from database import sqlite_db
from handlers.admin.admin_menu import admin_menu
from init import dp
from states.admin_states import EditStates


@dp.callback_query_handler(text="add_several_questions", state=EditStates.password_success)
async def admin_edit_questions(callback: types.CallbackQuery):
    await callback.message.delete_reply_markup()
    await EditStates.questions_text_request.set()
    await callback.message.answer(defines.ADMIN_MENU_EDIT_DESCRIPTION)


@dp.message_handler(state=EditStates.questions_text_request)
async def admin_get_txt_questions(message: types.Message):
    await sqlite_db.add_list_of_questions(message.text)
    await message.answer(defines.ADD_QUESTIONS_SUCCESS)
    await EditStates.password_success.set()
    await admin_menu(message)
