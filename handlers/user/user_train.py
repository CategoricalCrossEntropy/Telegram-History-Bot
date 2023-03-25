from aiogram import types
from aiogram.dispatcher import FSMContext, filters

import defines
from database import sqlite_db
from handlers.main_menu import main_menu
from init import dp
from keyboards.keyboard_builder import build_column_keyboard, build_select_keyboard
from scripts.false_answers_maker import get_variants


@dp.callback_query_handler(text="train_choose_theme")
async def user_choose_theme(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    themes = await sqlite_db.get_categories()
    async with state.proxy() as data:
        data["themes"] = themes
    if not themes:
        async with state.proxy() as data:
            data["category"] = None
        await init_train(callback, state)
        return
    await callback.message.answer(defines.CHOOSE_THEME_TO_REPEAT,
                                  reply_markup=build_select_keyboard(themes, prefix="theme"))


@dp.callback_query_handler(filters.Text(startswith="theme"))
async def call_init(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["category"] = data["themes"][int(callback.data.replace("theme", ""))]
    await init_train(callback, state)


@dp.callback_query_handler(text="init_train")
async def init_train(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    async with state.proxy() as data:
        data["questions_asked"] = data["correct_answers"] = 0
        several_questions = await sqlite_db.select_n_random_questions(defines.NUMBER_OF_QUESTIONS,
                                                                      category=data["category"])
        if len(several_questions) == 0:
            await callback.message.answer(defines.THERE_IS_NO_QUESTIONS_IN_DB)
            await state.finish()
            await main_menu(callback.message)
            return
        data["num_of_questions"] = min(len(several_questions), defines.NUMBER_OF_QUESTIONS)
        data["several_questions"] = several_questions
        data["user_hp"] = await sqlite_db.get_hp_by_user_id(callback.from_user.id)
    await train(callback, state)


@dp.callback_query_handler(text="train")
async def train(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if data["questions_asked"] >= data["num_of_questions"]:
            await results(callback, state)
            return
        question, answer = data["several_questions"][data["questions_asked"]]
        data["current_question"], data["current_answer"] = question, answer
        data["questions_asked"] += 1
        answers, callbacks = await get_variants(answer, defines.NUMBER_OF_VARIANTS, "correct", "incorrect")
    answers.append(defines.BACK_TO_MENU)
    callbacks.append("cancel")
    await callback.message.answer(defines.ANSWER_THE_QUESTION.format(question),
                                  reply_markup=build_column_keyboard(answers, callbacks))


@dp.callback_query_handler(text="correct")
async def correct_answer(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    async with state.proxy() as data:
        data["correct_answers"] += 1
        text = defines.ANSWER_THE_QUESTION.format(data["current_question"]) + "\n"
        text += defines.CORRECT.format(data["current_answer"])
        await callback.message.answer(text)
    await train(callback, state)


@dp.callback_query_handler(text="incorrect")
async def incorrect_answer(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    async with state.proxy() as data:
        text = defines.ANSWER_THE_QUESTION.format(data["current_question"]) + "\n"
        text += defines.INCORRECT.format(data["current_answer"])
        await callback.message.answer(text)
    await train(callback, state)


@dp.callback_query_handler(text="results")
async def results(callback: types.CallbackQuery, state: FSMContext):
    answers = [defines.TRAIN_AGAIN, defines.BACK_TO_MENU]
    callbacks = ["init_train", "cancel"]
    async with state.proxy() as data:
        data["user_hp"] += data["correct_answers"]
        result = defines.RESULT.format(data["correct_answers"], data["questions_asked"], data["user_hp"])
    await sqlite_db.set_user_hp(callback.from_user.id, data["user_hp"])
    await callback.message.answer(result, reply_markup=build_column_keyboard(answers, callbacks))
