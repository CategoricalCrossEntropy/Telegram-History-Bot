from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def build_column_keyboard(array, callback=None, links=None):
    if callback is None:
        callback = array
    if links is None:
        links = [None for _ in array]
    buttons_list = [InlineKeyboardButton(text=text, callback_data=action, url=link)
                    for text, action, link in zip(array, callback, links)]
    buttons_list = [[i] for i in buttons_list]
    return InlineKeyboardMarkup(inline_keyboard=buttons_list)
