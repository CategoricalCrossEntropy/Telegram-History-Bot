from aiogram import types

import defines
from database import sqlite_db
from handlers.admin.admin_menu import admin_menu
from init import dp
from states.admin_states import EditStates


@dp.callback_query_handler(text="delete_question", state=EditStates.password_success)
async def admin_delete_questions_desc(callback: types.CallbackQuery):
    await callback.message.delete_reply_markup()
    await EditStates.questions_del_num_request.set()
    await callback.message.answer(defines.ADMIN_MENU_DELETE_DESCRIPTION)


@dp.message_handler(state=EditStates.questions_del_num_request)
async def admin_delete_questions(message: types.Message):
    request = message.text
    try:
        if request == "0":
            pass
        elif request == "*":
            await sqlite_db.delete_questions()
            await message.answer(defines.DELETE_QUESTIONS_SUCCESS)
        else:
            await sqlite_db.delete_several_questions(request)
            await message.answer(defines.DELETE_QUESTIONS_SUCCESS)
        await EditStates.password_success.set()
        await admin_menu(message)
    except IndexError:
        await message.answer("В базе данных нет вопроса с таким номером")
        return
    except ValueError:
        await message.answer("Некорректно указаны номера вопросов")
