from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(StatesGroup):
    password_request = State()
