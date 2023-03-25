from aiogram import types

import defines
from database import sqlite_db
from init import dp
from keyboards.keyboard_builder import build_column_keyboard


@dp.callback_query_handler(text="user_profile")
async def user_profile(callback: types.CallbackQuery):
    await callback.message.delete()
    answers = [defines.START_TRAIN, defines.BACK_TO_MENU]
    callbacks = ["train_choose_theme", "cancel"]
    hp = await sqlite_db.get_hp_by_user_id(callback.from_user.id)
    await callback.message.answer(defines.USER_PROFILE_DESC.format(callback.from_user.first_name, hp),
                                  reply_markup=build_column_keyboard(answers, callbacks))
