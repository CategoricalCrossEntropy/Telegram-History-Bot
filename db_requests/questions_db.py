import sqlite3 as sq


class Questions:
    def __init__(self):
        self.base = sq.connect("databases/bot_data.db")
        self.cur = self.base.cursor()
        self.base.execute('CREATE TABLE IF NOT EXISTS questions(question TEXT, answer TEXT, category TEXT)')
        self.base.commit()

    async def add_question(self, question, answer, category):
        self.cur.execute('INSERT INTO questions VALUES (?, ?, ?)', (str(question), str(answer).lower(), str(category)))
        self.base.commit()

    async def select_n_random_questions(self, n, category=None):
        if category is None:
            request = "SELECT question, answer FROM questions ORDER BY RANDOM() LIMIT {}".format(n)
        else:
            request = 'SELECT question, answer FROM questions WHERE category="{}" ' \
                      'ORDER BY RANDOM() LIMIT {}'.format(category, n)
        questions = self.cur.execute(request).fetchall()
        return questions

    async def get_all_questions(self):
        questions = self.cur.execute('SELECT question, answer, category FROM questions').fetchall()
        return questions

    async def get_categories(self):
        categories = self.cur.execute('SELECT DISTINCT category FROM questions WHERE category!="-"').fetchall()
        if not categories:
            return None
        return [category[0] for category in categories]

    async def delete_questions(self):
        self.cur.execute('DELETE FROM questions')
        self.base.commit()

    async def delete_by_name(self, name):
        req = "DELETE FROM questions WHERE question='{}'".format(name)
        self.cur.execute(req)
        self.base.commit()

    async def get_questions_by_category(self, category):
        questions = self.cur.execute('''SELECT question, answer, category
                                         FROM questions WHERE category="{}"'''.format(category)).fetchall()
        return questions

    async def get_by_numbers(self, numbers: list):
        questions = await self.get_all_questions()
        questions = [questions[i - 1][0] for i in numbers]
        return questions

    async def delete_several_questions(self, request):
        request = list(map(int, request.replace(" ", "").split(",")))
        questions = await self.get_by_numbers(request)
        for q in questions:
            await self.delete_by_name(q)

    async def add_list_of_questions(self, text):
        for question in text.split("\n\n"):
            category, question, answer = question.split("\n")
            await self.add_question(question, answer, category)
