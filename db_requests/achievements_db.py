import sqlite3 as sq


class Achievements:
    def __init__(self):
        self.base = sq.connect("databases/bot_data.db")
        self.cur = self.base.cursor()
        self.base.execute('CREATE TABLE IF NOT EXISTS achievements('
                          'description TEXT, '
                          'link TEXT, '
                          'hp_to_receive INTEGER'
                          ')')
        self.base.commit()

    async def add_achievement(self, description, link=None, hp_to_receive=0):
        self.cur.execute("INSERT INTO achievements VALUES ('{}', '{}', '{}')".format(description, link, hp_to_receive))
        self.base.commit()

    async def get_all_achievements(self):
        achievements = self.cur.execute('SELECT description, link, hp_to_receive FROM achievements').fetchall()
        return achievements

    async def get_achievements_by_hp(self, hp):
        achievements = self.cur.execute('SELECT description, link, hp_to_receive '
                                        'FROM achievements '
                                        'WHERE hp_to_receive <= {}'.format(hp)).fetchall()
        return achievements

    async def delete_all_achievements(self):
        self.cur.execute('DELETE FROM achievements')
        self.base.commit()

    async def set_list_of_achievements(self, text):
        await self.delete_all_achievements()
        for achievement in text.split("\n\n"):
            description, link, hp_to_receive = achievement.split("\n")
            if link in ("-", "–", "—", "_", "None"):
                link = None
            await self.add_achievement(description, link, hp_to_receive)
