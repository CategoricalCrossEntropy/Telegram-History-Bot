import sqlite3 as sq


class Codeword:
    def __init__(self):
        self.base = sq.connect("databases/bot_data.db")
        self.cur = self.base.cursor()
        self.base.execute('CREATE TABLE IF NOT EXISTS codewords(codeword TEXT PRIMARY KEY, info TEXT)')
        self.base.commit()

    async def codeword_is_empty(self):
        return self.cur.execute('SELECT COUNT(*) FROM codewords').fetchall()[0][0] == 0

    async def get_codeword(self):
        return self.cur.execute('SELECT codeword FROM codewords').fetchone()[0]

    async def del_codeword(self):
        self.cur.execute('DELETE FROM codewords')
        self.base.commit()

    async def set_new_codeword(self, new_codeword, info=None):
        await self.del_codeword()
        self.cur.execute("INSERT INTO codewords VALUES ('{}', '{}')".format(new_codeword, info))
        self.base.commit()
