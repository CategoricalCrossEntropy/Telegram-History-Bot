from aiogram import types
from aiogram.dispatcher import FSMContext

import defines
from database import sqlite_db
from handlers.admin.admin_menu import admin_menu
from init import dp
from states.admin_states import EditStates


@dp.callback_query_handler(text="show_questions", state=EditStates.password_success)
async def admin_choose_category(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await EditStates.show_questions_choose_category.set()
    categories = await sqlite_db.get_categories()
    if not categories:
        await callback.message.answer(defines.SELECT_THE_CATEGORY)
        return
    async with state.proxy() as data:
        data["categories"] = categories
    cat_list = defines.SELECT_THE_CATEGORY + "\n"
    for ind, category in enumerate(categories):
        cat_list += "{}){}\n".format(ind+1, category)
    await callback.message.answer(cat_list)


@dp.message_handler(state=EditStates.show_questions_choose_category, text="*")
async def admin_show_questions(message: types.Message, state: FSMContext, category=None):
    if category is None:
        questions = await sqlite_db.get_all_questions()
    else:
        questions = await sqlite_db.get_questions_by_category(category)
    text = ""
    for i, qa in enumerate(questions):
        if category is not None:
            text += "{} ({})\n✅{}\n".format(qa[0], qa[2], qa[1])
        else:
            text += "{}){} ({})\n✅{}\n".format(i + 1, qa[0], qa[2], qa[1])
        text += "\n\n"
    if len(text) == 0:
        await message.answer("В базе данных нет вопросов")
    elif len(text) > defines.MAX_MESSAGE_LEN:
        for x in range(0, len(text), defines.MAX_MESSAGE_LEN):
            await message.answer(text[x:x+defines.MAX_MESSAGE_LEN])
    else:
        await message.answer(text)
    await state.finish()
    await admin_menu(message)


@dp.message_handler(state=EditStates.show_questions_choose_category, text="#")
async def admin_show_machine_questions(message: types.Message, state: FSMContext):
    questions = await sqlite_db.get_all_questions()
    text = ""
    for i, qa in enumerate(questions):
        msg = "{}\n{}\n{}\n\n".format(qa[2], qa[0], qa[1])
        if len(text) + len(msg) >= defines.MAX_MESSAGE_LEN-1:
            await message.answer(text)
            text = msg
        else:
            text += msg
    await message.answer(text)
    await state.finish()
    await admin_menu(message)


@dp.message_handler(lambda msg: msg.text.isdigit(), state=EditStates.show_questions_choose_category)
async def admin_show_question_digit(message: types.Message, state: FSMContext):
    category_index = int(message.text) - 1
    async with state.proxy() as data:
        if len(data["categories"]) < category_index - 1:
            await message.answer(defines.INCORRECT_INPUT)
            return
        category = data["categories"][category_index]
    await admin_show_questions(message, state, category=category)


@dp.message_handler(state=EditStates.show_questions_choose_category)
async def admin_show_question_text(message: types.Message, state: FSMContext):
    await admin_show_questions(message, state, category=message.text)
