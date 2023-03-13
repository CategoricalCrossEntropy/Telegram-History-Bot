from aiogram import types

import defines
from database import sqlite_db
from init import dp
from states.admin_states import EditStates


@dp.callback_query_handler(text="show_questions", state=EditStates.password_success)
async def admin_show_question(callback: types.CallbackQuery):
    questions = await sqlite_db.get_all_questions()
    text = ""
    for i, qa in enumerate(questions):
        if qa[2] == "9":
            cat = "(9 класс)"
        elif qa[2] == "1":
            cat = "(10 класс)"
        else:
            cat = ""
        text += "{}){} {}\nОтвет: {}\n\n".format(i+1, qa[0], cat, qa[1])
    if len(text) == 0:
        await callback.message.answer("В базе данных нет вопросов")
        return
    if len(text) > defines.MAX_MESSAGE_LEN:
        for x in range(0, len(text), defines.MAX_MESSAGE_LEN):
            await callback.message.answer(text[x:x+defines.MAX_MESSAGE_LEN])
    else:
        await callback.message.answer(text)
