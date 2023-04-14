from aiogram import types
from aiogram.dispatcher import filters

import defines
from db_requests import Users_db, Achievements_db
from init import dp
from keyboards.keyboard_builder import build_column_keyboard


@dp.callback_query_handler(text="user_profile")
async def user_profile(callback: types.CallbackQuery):
    await callback.message.delete()
    answers, callbacks = [], []
    hp = await Users_db.get_hp_by_user_id(callback.from_user.id)
    achievements = await Achievements_db.get_achievements_by_hp(hp)
    if not achievements:
        text = defines.USER_PROFILE_DESC.format(callback.from_user.first_name, hp,
                                                defines.USER_PROFILE_ACHIEVEMENTS_EMPTY)
    else:
        achieve_text = ""
        subjects = []
        for i, (description, link, hp_to_receive, subject) in enumerate(achievements):
            achieve_text += defines.ACHIEVEMENT_TEMPLATE.format(subject, description, hp_to_receive)
            if link != "None" and subject not in subjects:
                subjects.append(subject)
        text = defines.USER_PROFILE_DESC.format(callback.from_user.first_name, hp,
                                                defines.USER_PROFILE_ACHIEVEMENTS.format(achieve_text))
        for subject in subjects:
            answers.append("Ссылки: {}".format(subject))
            callbacks.append("links_{}".format(subject))
    answers.extend([defines.START_TRAIN, defines.BACK_TO_MENU])
    callbacks.extend(["train_choose_theme", "cancel"])
    await callback.message.answer(text, reply_markup=build_column_keyboard(answers, callbacks))


@dp.callback_query_handler(filters.Text(startswith="links_"))
async def see_achievements_by_subject(callback: types.CallbackQuery):
    await callback.message.delete()
    subject = callback.data.replace("links_", "")
    hp = await Users_db.get_hp_by_user_id(callback.from_user.id)
    achievements = await Achievements_db.get_achievements_by_subject_hp(hp, subject)
    answers, callbacks, links = [], [], []
    for i, (description, link, hp_to_receive, _) in enumerate(achievements):
        answers.append("{} ({}⭐)".format(description, hp_to_receive))
        callbacks.append(None)
        links.append(link)
    answers.extend([defines.START_TRAIN, "Посмотреть все награды 🏅"])
    callbacks.extend(["train_choose_theme", "user_profile"])
    links.extend([None, None])
    text = "Твои награды по предмету: {}".format(subject)
    await callback.message.answer(text, reply_markup=build_column_keyboard(answers, callbacks, links))

