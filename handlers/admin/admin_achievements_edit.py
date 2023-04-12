from aiogram import types

import defines
from db_requests import Achievements_db
from handlers.admin.admin_menu import admin_menu
from init import dp
from states.admin_states import EditStates


@dp.callback_query_handler(text="edit_achievements", state=EditStates.password_success)
async def edit_achievements(callback: types.CallbackQuery):
    await callback.message.delete()
    await EditStates.new_achievements_request.set()
    achievements = await Achievements_db.get_all_achievements()
    current_column = ""
    for description, link, hp_to_receive in achievements:
        current_column += "{}\n{}\n{}\n\n".format(description, link, hp_to_receive)
    await callback.message.answer(defines.ADMIN_EDIT_ACHIEVEMENTS_DESCRIPTION.format(current_column))


@dp.message_handler(state=EditStates.new_achievements_request)
async def admin_get_achievements(message: types.Message):
    if message.text == "0":
        pass
    elif message.text == "*":
        await Achievements_db.delete_all_achievements()
        await message.answer(defines.ALL_ACHIEVEMENTS_DELETED)
    else:
        await Achievements_db.set_list_of_achievements(message.text)
        await message.answer(defines.SET_ACHIEVEMENTS_SUCCESS)
    await EditStates.password_success.set()
    await admin_menu(message)
