from aiogram.utils import executor

from database import sqlite_db
from init import dp
import handlers


async def on_startup(_):
    sqlite_db.sql_start()
    handlers.register()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
