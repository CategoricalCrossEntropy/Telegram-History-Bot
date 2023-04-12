import sqlite3 as sq


class Users:
    def __init__(self):
        self.base = sq.connect("databases/users.db")
        self.cur = self.base.cursor()
        self.base.execute('CREATE TABLE IF NOT EXISTS user(id TEXT PRIMARY KEY, hp INTEGER, register_status TEXT)')
        self.base.commit()

    async def user_in_database(self, id_):
        user = self.cur.execute('SELECT hp FROM user WHERE id={}'.format(id_)).fetchall()
        return bool(user)

    async def get_hp_by_user_id(self, id_):
        user = self.cur.execute('SELECT hp FROM user WHERE id={}'.format(id_)).fetchall()
        if not user:
            await self.add_user(id_)
            return 0
        return int(user[0][0])

    async def set_user_hp(self, id_, hp):
        self.cur.execute('UPDATE user SET hp={} WHERE id={}'.format(hp, id_))
        self.base.commit()

    async def add_user(self, id_, xp=0):
        self.cur.execute('INSERT INTO user VALUES (?, ?, ?)', (id_, xp, "registered"))
        self.base.commit()

    async def user_is_registered(self, id_):
        user = self.cur.execute('SELECT register_status FROM user WHERE id={}'.format(id_)).fetchall()
        if not user or user[0][0] == "unregistered":
            return False
        return True

    async def unregister_all(self):
        self.cur.execute("UPDATE user SET register_status = 'unregistered'")
        self.base.commit()

    async def register_user(self, id_):
        if await self.user_in_database(id_):
            self.cur.execute("UPDATE user SET register_status = 'registered' WHERE id={}".format(id_))
            self.base.commit()
            return
        await self.add_user(id_)
