from aiogram import types

from init import dp


@dp.message_handler(state="*")
async def unknown_command(message: types.Message):
    await message.answer("Неизвестная команда")
