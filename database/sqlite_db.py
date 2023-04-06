import sqlite3 as sq

from scripts.category_auto_detection import category_auto_detection


def sql_start():
    global base, cur
    base = sq.connect("questions.db")
    cur = base.cursor()
    base.execute('CREATE TABLE IF NOT EXISTS questions(question TEXT, answer TEXT, category TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS admin_id(id TEXT PRIMARY KEY)')
    base.execute('CREATE TABLE IF NOT EXISTS user(id TEXT PRIMARY KEY, hp INTEGER)')
    base.execute('CREATE TABLE IF NOT EXISTS links(link TEXT PRIMARY KEY, text TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS users_tmp(id TEXT PRIMARY KEY)')
    base.commit()


async def add_question(question, answer, category="auto"):
    if category == "auto":
        category = await category_auto_detection(answer)
    cur.execute('INSERT INTO questions VALUES (?, ?, ?)', (str(question), str(answer).lower(), str(category)))
    base.commit()


async def select_n_random_questions(n, category=None):
    if category is None:
        request = "SELECT question, answer FROM questions ORDER BY RANDOM() LIMIT {}".format(n)
    else:
        request = 'SELECT question, answer FROM questions WHERE category="{}" ' \
                  'ORDER BY RANDOM() LIMIT {}'.format(category, n)
    questions = cur.execute(request).fetchall()
    return questions


async def get_all_questions():
    questions = cur.execute('SELECT question, answer, category FROM questions').fetchall()
    return questions


async def add_admin(admin_id):
    cur.execute('INSERT INTO admin_id VALUES ({})'.format(admin_id))
    base.commit()


async def get_admins():
    ids = cur.execute('SELECT id FROM admin_id').fetchall()
    return [i[0] for i in ids]


async def delete_questions():
    cur.execute('DELETE FROM questions')
    base.commit()


async def delete_question_by_name(name):
    req = "DELETE FROM questions WHERE question='{}'".format(name)
    cur.execute(req)
    base.commit()


async def get_hp_by_user_id(id_):
    user = cur.execute('SELECT hp FROM user WHERE id={}'.format(id_)).fetchall()
    if not user:
        cur.execute('INSERT INTO user VALUES (?, ?)', (id_, 0))
        base.commit()
        return 0
    return int(user[0][0])


async def set_user_hp(id_, hp):
    cur.execute('UPDATE user SET hp={} WHERE id={}'.format(hp, id_))
    base.commit()


async def add_user(id_, xp=0):
    cur.execute('INSERT INTO user VALUES ({}, {})'.format(id_, xp))
    base.commit()


async def del_links():
    cur.execute('DELETE FROM links')
    base.commit()


async def set_links(links: dict):
    await del_links()
    for link, text in links.items():
        cur.execute("INSERT INTO links VALUES ('{}', '{}')".format(link, text))
    base.commit()


async def get_links():
    links = cur.execute('SELECT link, text FROM links')
    links = {i[0]: i[1] for i in links}
    return links


async def get_questions_by_numbers(numbers: list):
    questions = await get_all_questions()
    questions = [questions[i-1][0] for i in numbers]
    return questions


async def add_list_of_questions(text):
    for question in text.split("\n\n"):
        category, question, answer = question.split("\n")
        await add_question(question, answer, category)


async def delete_several_questions(request):
    request = list(map(int, request.replace(" ", "").split(",")))
    questions = await get_questions_by_numbers(request)
    for q in questions:
        await delete_question_by_name(q)


async def get_categories():
    categories = cur.execute('SELECT DISTINCT category FROM questions WHERE category!="-"').fetchall()
    if not categories:
        return None
    return [category[0] for category in categories]


async def get_questions_by_category(category):
    questions = cur.execute('''SELECT question, answer, category
                                 FROM questions WHERE category="{}"'''.format(category)).fetchall()
    return questions


async def get_users_tmp():
    ids = cur.execute('SELECT id FROM users_tmp').fetchall()
    return [i[0] for i in ids]


async def add_user_tmp(user_id):
    cur.execute('INSERT INTO users_tmp VALUES ({})'.format(user_id))
    base.commit()
