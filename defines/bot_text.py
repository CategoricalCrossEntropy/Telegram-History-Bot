START_COMMAND = "Пройти тест"
SHOW_ALL_DATES = "Показать все даты 🏻"
CANCEL_COMMAND = "Назад ↩"
GREETING = "Добро пожаловать в бот 988: тренажер дат 🗓\n\n"\
           "Со мной ты можешь потренироваться в повторении дат по истории и круто подготовиться к экзамену ❤\n\n"\
           "Начнём подготовку? 👇🏻"
ENTER_KEYWORD = "Введи, пожалуйста, кодовое слово:"
CORRECT_KEYWORD = "Успешная авторизация!"
ALREADY_AUTHORIZED = "Вы уже авторизованы"

START_TRAIN = "Поехали! 🚀"
USER_PROFILE = "Мой профиль ⭐"
USER_PROFILE_DESC = "Добро пожаловать в свой профиль, {}! 🤗\n\n" \
                    "Сейчас у тебя {} XP ⭐\n\n" \
                    "Давай тренироваться дальше! 💻"
CHOOSE_THEME_TO_REPEAT = "Выбери тему, которую хочешь повторить:"
THERE_IS_NO_QUESTIONS_IN_DB = "Вопросов для повторения пока нет 🥴"
MESSAGE_TO_ADMIN = "Написать сообщение администратору ❤"
TRAIN_AGAIN = "Заново 👈🏻"
BACK_TO_MENU = "Вернуться в главное меню 🧑🏻‍💻"
SELECT_ALL = "Выбрать всё ⬆"
ANSWER_THE_QUESTION = "Выбери дату: {}"
CORRECT = "✅ Правильно!\nОтвет: {}"
INCORRECT = "❌ Неверно 🥺\n✅ Правильный ответ: {}"
RESULT = "Твой результат: {} из {}.\nНакоплено {} XP ⭐\n\n"\
         "Пошли практиковаться дальше! 🏃🏽‍♀"
PASSWORD_REQUEST_USER = "Введи кодовое слово для использования бота:"

PASSWORD_REQUEST = "Вы не являетесь администратором бота\n"\
                   "Введите пароль для авторизации:"
ADMIN_MENU_TEXT = "Добро пожаловать в меню администратора!\n"\
    "Здесь вы можете добавлять, удалять, редактировать вопросы."
ADMIN_MENU_ADD = "Добавить вопрос ✅"
ADMIN_MENU_DELETE = "Удалить вопрос(ы) ❌"

ENTER_THE_CATEGORY = "Добавление вопроса:\n" \
                     "Если вопрос не имеет темы, введите '-'\n" \
                     "✅ -\n\n" \
                     "Для возврата в меню администратора введите '0'\n" \
                     "✅ 0\n\n" \
                     "Для добавления набора вопросов в машинном виде введите '#'\n" \
                     "✅ #\n\n" \
                     "{}"
ENTER_MACHINE_QUESTIONS = '''Введите набор вопросов в машинном виде:'''
ENTER_THE_CATEGORY_ZERO = "Введите тему(категорию) вопроса:"
ENTER_THE_CATEGORY_SEVERAL = "Введите или выберете тему(категорию) вопроса:"
ENTER_THE_CATEGORY_MANY = "Введите тему(категорию) вопроса или введите его номер из списка:\n\n"
ENTER_THE_QUESTION = "Введите текст вопроса, который хотите добавить:"
ENTER_THE_ANSWER = "Введите ответ на вопрос:"
ADD_QUESTION_SUCCESS = "Вопрос успешно добавлен!"
ADD_QUESTIONS_SUCCESS = "Вопросы успешно добавлены!"
DELETE_QUESTIONS_SUCCESS = "Вопросы успешно удалены!"
INCORRECT_INPUT = "Некорректный ввод"
ADMIN_MENU_DELETE_TEXT = "Все вопросы были удалены"
ADMIN_MENU_SHOW = "Посмотреть все вопросы 🧐"
ADMIN_MENU_MULTI_ADD = "Добавить список вопросов 📝"
ADMIN_MENU_LINKS_EDIT = "Редактировать ссылки в главном меню 🔗"
ALL_LINKS_DELETED = "✅ Все ссылки удалены"
INCORRECT_LINKS_LENGTH = "❌ Для ввода ссылок должно быть чётное число строк"
SET_LINKS_SUCCESS = "✅ Все ссылки успешно заменены"
ADMIN_MENU_EDIT_DESCRIPTION = "Эта команда добавляет список вопросов к базе данных\n\n"\
                              "Вопросы, ранее хранившиеся в базе данных НЕ будут удалены!\n\n"\
                              "Вставьте сюда текст с любым количеством вопросов:\n"
ADMIN_MENU_DELETE_DESCRIPTION = "Эта команда удаляет один или несколько вопросов из базы данных.\n\n"\
                                "Для удаления нескольких вопросов, введите их порядковые номера через запятую:\n"\
                                "✅ 3, 6, 12, 13\n\n"\
                                "Чтобы удалить один вопрос, введите его порядковый номер:\n"\
                                "✅ 3\n\n"\
                                "Чтобы удалить все вопросы в базе данных, введите символ '*':\n"\
                                "✅ *\n\n"\
                                "Если вы не хотите ничего удалять, напишите 0:\n"\
                                "✅ 0\n\n"\
                                "Укажите вопросы, которые хотите удалить:"
ADMIN_EDIT_LINKS_DESCRIPTION = "Эта команда заменяет ссылки в главном меню.\n\n"\
                               "Для установки новых ссылок введите текст в следующем формате:\n"\
                               "Текст ссылки №1[перенос на новую строку]\n"\
                               "Ссылка №1[перенос на новую строку]\n"\
                               "Текст ссылки №2[перенос на новую строку]\n"\
                               "Ссылка №2[перенос на новую строку]\n\n"\
                               "{}"\
                               "Если вы хотите удалить все ссылки, введите '*'\n"\
                               "✅ *\n\n"\
                               "Чтобы выйти из меню редактирования ссылок, введите '0'\n"\
                               "✅ 0\n\n"\
                               "Введите запрос:"
LINKS_EXAMPLE = "✅ Пример:\n"\
                "Ссылка на телеграм\n"\
                "https://web.telegram.org/\n"\
                "Ссылка на Гугл\n"\
                "https://www.google.com/\n\n"
CURRENT_LINKS = "☑ Актуальные ссылки:\n"
SELECT_THE_CATEGORY = "Введите номер категории из списка ниже, или введите\n" \
                      "'*' для просмотре всех вопросов\n" \
                      "'#' для просмотра и копирования вопросов в машинном виде.\n"
