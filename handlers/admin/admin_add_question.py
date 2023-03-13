from aiogram import types
from aiogram.dispatcher import FSMContext

import defines
from database import sqlite_db
from handlers.admin.admin_menu import admin_menu
from init import dp
from states.admin_states import EditStates


@dp.callback_query_handler(text="add_question", state=EditStates.password_success)
async def admin_edit_questions(callback: types.CallbackQuery):
    await callback.message.delete_reply_markup()
    await EditStates.add_answer.set()
    await callback.message.answer(defines.ENTER_THE_QUESTION)


@dp.message_handler(state=EditStates.add_answer)
async def admin_add_answer(message: types.Message, state: FSMContext):
    await state.update_data(question=message.text)
    await EditStates.add_question_success.set()
    await message.answer(defines.ENTER_THE_ANSWER)


@dp.message_handler(state=EditStates.add_question_success)
async def admin_add_question_success(message: types.Message, state: FSMContext):
    await state.update_data(answer=message.text)
    q_data = await state.get_data()
    await sqlite_db.add_question(q_data["question"], q_data["answer"])
    await state.finish()
    await message.answer(defines.ADD_QUESTION_SUCCESS)
    await admin_menu(message)
