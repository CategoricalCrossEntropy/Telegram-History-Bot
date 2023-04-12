from aiogram import types

import defines
from db_requests import Codeword_db, Users_db
from handlers.admin.admin_menu import admin_menu
from init import dp
from keyboards.keyboard_builder import build_column_keyboard
from states.admin_states import EditStates


@dp.callback_query_handler(text="set_codeword", state=EditStates.password_success)
async def set_codeword(callback: types.CallbackQuery):
    await callback.message.delete()
    if await Codeword_db.codeword_is_empty():
        codeword = defines.EMPTY_CODEWORD
    else:
        codeword = await Codeword_db.get_codeword()
    texts = [defines.SET_NEW_CODEWORD, defines.BACK_TO_MENU]
    callbacks = ["set_new_codeword", "admin_cancel"]
    await callback.message.answer(defines.SET_CODEWORD_DESCRIPTION.format(codeword),
                                  reply_markup=build_column_keyboard(texts, callbacks))


@dp.callback_query_handler(text="set_new_codeword", state=EditStates.password_success)
async def enter_codeword(callback: types.CallbackQuery):
    await callback.message.delete()
    await EditStates.new_codeword_request.set()
    await callback.message.answer(defines.SET_NEW_CODEWORD_DESCRIPTION)


@dp.message_handler(state=EditStates.new_codeword_request)
async def upload_new_codeword(message: types.Message):
    if message.text == "0":
        pass
    else:
        await Codeword_db.set_new_codeword(message.text)
        await Users_db.unregister_all()
    await EditStates.password_success.set()
    await admin_menu(message)
