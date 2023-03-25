from aiogram import types
from aiogram.dispatcher import FSMContext

import defines
from database import sqlite_db
from handlers.admin.admin_menu import admin_menu
from init import dp
from states.admin_states import EditStates


@dp.callback_query_handler(text="add_question", state=EditStates.password_success)
async def admin_add_question(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await EditStates.add_question.set()
    categories = await sqlite_db.get_categories()
    async with state.proxy() as data:
        data["categories"] = categories
    if not categories:
        await callback.message.answer(defines.ENTER_THE_CATEGORY.format(defines.ENTER_THE_CATEGORY_ZERO))
    else:
        cat_list = ""
        for ind, val in enumerate(categories):
            cat_list += "{}){}\n".format(ind+1, val)
        await callback.message.answer(defines.ENTER_THE_CATEGORY.format(defines.ENTER_THE_CATEGORY_MANY) + cat_list)


@dp.message_handler(state=EditStates.add_question, text="0")
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await admin_menu(message)


@dp.message_handler(state=EditStates.add_question, text="#")
async def add_machine_questions_desc(message: types.Message):
    await message.answer(defines.ENTER_MACHINE_QUESTIONS)
    await EditStates.add_machine_questions.set()


@dp.message_handler(state=EditStates.add_machine_questions)
async def add_machine_questions(message: types.Message, state: FSMContext):
    for question in message.text.split("\n\n"):
        category, question, answer, *wrong_answers = question.split("\n")
        await sqlite_db.add_question(question, answer, category)
    await state.finish()
    await message.answer(defines.ADD_QUESTIONS_SUCCESS)
    await admin_menu(message)


@dp.message_handler(state=EditStates.add_question)
async def admin_add_question_text(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        category_index = int(message.text) - 1
        async with state.proxy() as data:
            if len(data["categories"]) < category_index - 1:
                await message.answer(defines.INCORRECT_INPUT)
                return
            category = data["categories"][category_index]
    else:
        category = message.text
    async with state.proxy() as data:
        data["category"] = "-" if category in ["-", "—"] else category
    await EditStates.add_answer.set()
    await message.answer(defines.ENTER_THE_QUESTION)


@dp.message_handler(state=EditStates.add_answer)
async def admin_add_answer(message: types.Message, state: FSMContext):
    await state.update_data(question=message.text)
    await EditStates.add_question_success.set()
    await message.answer(defines.ENTER_THE_ANSWER)


@dp.message_handler(state=EditStates.add_question_success)
async def admin_add_question_success(message: types.Message, state: FSMContext):
    answer = message.text
    async with state.proxy() as data:
        await sqlite_db.add_question(data["question"], answer, data["category"])
        text = defines.ADD_QUESTION_SUCCESS
        text += "{}({})\n✅{}\n".format(data["question"], data["category"], answer)
    await state.finish()
    await message.answer(text)
    await admin_menu(message)
