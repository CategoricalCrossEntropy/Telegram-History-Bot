from aiogram import types
from aiogram.dispatcher import FSMContext

import defines
from database import sqlite_db
from handlers.main_menu import main_menu
from init import dp
from keyboards.keyboard_builder import build_column_keyboard
from scripts.false_answers_maker import get_variants


@dp.callback_query_handler(text="train_9")
async def init_train_9(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(class_category=9)
    await init_train(callback, state)


@dp.callback_query_handler(text="train_10")
async def init_train_10(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(class_category=10)
    await init_train(callback, state)


@dp.callback_query_handler(text="init_train")
async def init_train(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    async with state.proxy() as data:
        data["num_of_questions"] = defines.NUMBER_OF_QUESTIONS
        data["questions_asked"] = data["correct_answers"] = 0
        category = 9 if data["class_category"] == 9 else None
        several_questions = await sqlite_db.select_n_random_questions(defines.NUMBER_OF_QUESTIONS, category)
        data["several_questions"] = several_questions
        data["user_hp"] = await sqlite_db.get_hp_by_user_id(callback.from_user.id)
    await train(callback, state)


@dp.callback_query_handler(text="train")
async def train(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if data["questions_asked"] >= defines.NUMBER_OF_QUESTIONS:
            await results(callback, state)
            return
        question, answer = data["several_questions"][data["questions_asked"]]
        data["questions_asked"] += 1
    answers, callbacks = await get_variants(answer, defines.NUMBER_OF_VARIANTS,
                                            correct="correct", incorrect="incorrect")
    answers.append(defines.BACK_TO_MENU)
    callbacks.append("cancel")
    await callback.message.answer(defines.ANSWER_THE_QUESTION + question,
                                  reply_markup=build_column_keyboard(answers, callbacks))


@dp.callback_query_handler(text="correct")
async def correct_answer(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    async with state.proxy() as data:
        question, answer = data["several_questions"][data["questions_asked"]-1]
        data["correct_answers"] += 1
    await callback.message.answer(defines.CORRECT.format(answer))
    await train(callback, state)


@dp.callback_query_handler(text="incorrect")
async def incorrect_answer(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    async with state.proxy() as data:
        question, answer = data["several_questions"][data["questions_asked"]-1]
    await callback.message.answer(defines.INCORRECT.format(answer))
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


@dp.callback_query_handler(text="cancel")
async def _cancel(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    await state.finish()
    await main_menu(callback.message)
