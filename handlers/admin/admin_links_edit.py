from aiogram import types

import defines
from database import sqlite_db
from handlers.admin.admin_menu import admin_menu
from init import dp
from states.admin_states import EditStates


@dp.callback_query_handler(text="edit_links", state=EditStates.password_success)
async def edit_links(callback: types.CallbackQuery):
    await callback.message.delete_reply_markup()
    await EditStates.new_links_request.set()
    await callback.message.answer(defines.ADMIN_EDIT_LINKS_DESCRIPTION)


@dp.message_handler(state=EditStates.new_links_request)
async def admin_get_txt_questions(message: types.Message):
    if message.text == "0":
        pass
    elif message.text == "*":
        await sqlite_db.del_links()
        await message.answer(defines.ALL_LINKS_DELETED)
    else:
        links = message.text
        links = links.split("\n")
        if len(links) % 2 == 1:
            await message.answer(defines.INCORRECT_LINKS_LENGTH)
            return
        links = {links[i+1]: links[i] for i in range(0, len(links), 2)}
        await sqlite_db.set_links(links)
        await message.answer(defines.SET_LINKS_SUCCESS)
    await EditStates.password_success.set()
    await admin_menu(message)
