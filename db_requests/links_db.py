import sqlite3 as sq


class Links:
    def __init__(self):
        self.base = sq.connect("databases/bot_data.db")
        self.cur = self.base.cursor()
        self.base.execute('CREATE TABLE IF NOT EXISTS links(link TEXT, text TEXT)')
        self.base.commit()

    async def set_links(self, links: dict):
        await self.del_links()
        for link, text in links.items():
            self.cur.execute("INSERT INTO links VALUES ('{}', '{}')".format(link, text))
        self.base.commit()

    async def del_links(self):
        self.cur.execute('DELETE FROM links')
        self.base.commit()

    async def get_links(self):
        links = self.cur.execute('SELECT link, text FROM links').fetchall()
        links = {i[0]: i[1] for i in links}
        return links
