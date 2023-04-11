from aiogram.utils import executor

import db_requests
from init import dp
import handlers


async def on_startup(_):
    handlers.register()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
