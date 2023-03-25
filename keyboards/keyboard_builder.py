from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import defines


def build_column_keyboard(array, callback=None, links=None):
    if callback is None:
        callback = array
    if links is None:
        links = [None for _ in array]
    buttons_list = [InlineKeyboardButton(text=text, callback_data=action, url=link)
                    for text, action, link in zip(array, callback, links)]
    buttons_list = [[i] for i in buttons_list]
    return InlineKeyboardMarkup(inline_keyboard=buttons_list)


def build_select_keyboard(array, prefix="", start_val=0, add_select_all=False, cancel_callback="cancel",
                          select_all_callback="select_all"):
    buttons_list = [InlineKeyboardButton(text=text, callback_data=prefix+str(start_val+index))
                    for index, text in enumerate(array)]
    buttons_list = [[i] for i in buttons_list]
    if add_select_all:
        buttons_list.append([InlineKeyboardButton(text=defines.SELECT_ALL, callback_data=select_all_callback)])
    buttons_list.append([InlineKeyboardButton(text=defines.BACK_TO_MENU, callback_data=cancel_callback)])
    return InlineKeyboardMarkup(inline_keyboard=buttons_list)
