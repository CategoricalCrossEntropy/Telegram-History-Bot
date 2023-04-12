from aiogram import types

import defines
from db_requests import Users_db, Achievements_db
from init import dp
from keyboards.keyboard_builder import build_column_keyboard


@dp.callback_query_handler(text="user_profile")
async def user_profile(callback: types.CallbackQuery):
    await callback.message.delete()
    answers = [defines.START_TRAIN, defines.BACK_TO_MENU]
    callbacks = ["train_choose_theme", "cancel"]
    links = [None, None]
    hp = await Users_db.get_hp_by_user_id(callback.from_user.id)
    achievements = await Achievements_db.get_achievements_by_hp(hp)
    if not achievements:
        text = defines.USER_PROFILE_DESC.format(callback.from_user.first_name, hp,
                                                defines.USER_PROFILE_ACHIEVEMENTS_EMPTY)
    else:
        achieve_text = ""
        for i, (description, link, hp_to_receive) in enumerate(achievements):
            achieve_text += defines.ACHIEVEMENT_TEMPLATE.format(i+1, description, hp_to_receive)
            if link != "None":
                answers.append(description)
                callbacks.append(None)
                links.append(link)
        text = defines.USER_PROFILE_DESC.format(callback.from_user.first_name, hp,
                                                defines.USER_PROFILE_ACHIEVEMENTS.format(achieve_text))
    await callback.message.answer(text, reply_markup=build_column_keyboard(answers, callbacks, links))
