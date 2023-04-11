import sqlite3 as sq


class Admins:
    def __init__(self):
        self.base = sq.connect("databases/users.db")
        self.cur = self.base.cursor()
        self.base.execute('CREATE TABLE IF NOT EXISTS admins(id TEXT PRIMARY KEY)')
        self.base.commit()

    async def add_admin(self, admin_id):
        self.cur.execute('INSERT INTO admins VALUES ({})'.format(admin_id))
        self.base.commit()

    async def get_admins(self):
        ids = self.cur.execute('SELECT id FROM admins').fetchall()
        return [i[0] for i in ids]
