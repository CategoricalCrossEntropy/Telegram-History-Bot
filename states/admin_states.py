from aiogram.dispatcher.filters.state import StatesGroup, State


class EditStates(StatesGroup):
    password_request = State()
    password_success = State()
    add_answer = State()
    add_question_success = State()
    add_several_questions = State()
    questions_text_request = State()
    questions_del_num_request = State()
    new_links_request = State()
    add_question = State()
    add_category = State()
    show_questions_choose_category = State()
    add_machine_questions = State()
