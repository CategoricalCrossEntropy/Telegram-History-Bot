import sqlite3 as sq


class Users:
    def __init__(self):
        self.base = sq.connect("databases/users.db")
        self.cur = self.base.cursor()
        self.base.execute('CREATE TABLE IF NOT EXISTS user(id TEXT PRIMARY KEY, hp INTEGER, register_status TEXT)')
        self.base.commit()

    async def get_hp_by_user_id(self, id_):
        user = self.cur.execute('SELECT hp FROM user WHERE id={}'.format(id_)).fetchall()
        if not user:
            self.cur.execute('INSERT INTO user VALUES (?, ?, ?)', (id_, 0, "registered"))
            self.base.commit()
            return 0
        return int(user[0][0])

    async def set_user_hp(self, id_, hp):
        self.cur.execute('UPDATE user SET hp={} WHERE id={}'.format(hp, id_))
        self.base.commit()

    async def add_user(self, id_, xp=0):
        self.cur.execute('INSERT INTO user VALUES ({}, {})'.format(id_, xp))
        self.base.commit()
