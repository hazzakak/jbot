import logging

import aiosqlite

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class Database:
    def __init__(self, database_path):
        self.database_path = database_path


class ReactRoles(Database):
    def __init__(self):
        Database.__init__(self, 'utilities/databases/react.db')

    async def add_list(self, name, roles: list, guild):
        async with aiosqlite.connect(self.database_path) as db:
            sql = f'INSERT INTO role_messages (name, roles, guild_id) VALUES (?, ?, ?)'
            await db.execute(sql, (name, repr(roles), guild,))
            await db.commit()

    async def update_message_id(self, name, message_id):
        async with aiosqlite.connect(self.database_path) as db:
            sql = f'UPDATE role_messages SET message_id=? WHERE name = ?'
            await db.execute(sql, (message_id, name,))
            await db.commit()

    async def get_lists(self, guild):
        async with aiosqlite.connect(self.database_path) as db:
            db.row_factory = aiosqlite.Row
            sql = f'SELECT * FROM role_messages WHERE guild_id = ?'
            cursor = await db.execute(sql, (guild,))
            cursor = await cursor.fetchall()
            return cursor

    async def get_list_by_name(self, name):
        async with aiosqlite.connect(self.database_path) as db:
            db.row_factory = aiosqlite.Row
            sql = f'SELECT * FROM role_messages WHERE name = ?'
            cursor = await db.execute(sql, (name,))
            cursor = await cursor.fetchone()
            return cursor

    async def get_list_by_msg(self, message_id):
        async with aiosqlite.connect(self.database_path) as db:
            db.row_factory = aiosqlite.Row
            sql = f'SELECT * FROM role_messages WHERE message_id = ?'
            cursor = await db.execute(sql, (message_id,))
            cursor = await cursor.fetchone()

            return cursor


class Tickets:
    async def add_server(self, id):
        async with aiosqlite.connect('utilities/databases/tickets.db') as db:
            try:
                sql = f'''CREATE TABLE server_{id} (
                    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                    `roles` TEXT,
                    `name` TEXT,
                    `message_id` INTEGER,
                    `info_message_id` INTEGER,
                    `info_message` TEXT);
                    '''
                cursor = await db.execute(sql)
                await db.commit()
                return cursor.lastrowid
            except:
                print("error")

            try:
                sql = f'INSERT INTO servers (serverid) VALUES (?)'
                cursor = await db.execute(sql, (id,))
                await db.commit()
            except:
                print("error")

    async def get_tickets(self, serverid):
        async with aiosqlite.connect('utilities/databases/tickets.db') as db:
            db.row_factory = aiosqlite.Row
            sql = f'SELECT * FROM server_{serverid}'
            cursor = await db.execute(sql)
            return await cursor.fetchall()

    async def add_tickets(self, roles, name, serverid, info_message):
        async with aiosqlite.connect('utilities/databases/tickets.db') as db:
            sql = f'INSERT INTO server_{serverid} (roles, name, message_id, info_message) VALUES (?, ?, ?, ?)'
            cursor = await db.execute(sql, (str(roles), str(name), 0, info_message,))
            await db.commit()
            return cursor.lastrowid

    async def add_ticket_number(self, serverid):
        async with aiosqlite.connect('utilities/databases/tickets.db') as db:
            sql = f'UPDATE servers SET tickets=tickets+1 WHERE serverid = ?'
            cursor = await db.execute(sql, (serverid,))
            await db.commit()

    async def get_log_channel(self, serverid):
        async with aiosqlite.connect('utilities/databases/tickets.db') as db:
            db.row_factory = aiosqlite.Row
            sql = f'SELECT log_channel FROM servers WHERE serverid = ?'
            cursor = await db.execute(sql, (serverid,))
            cursor = await cursor.fetchone()
            return cursor

    async def get_ticket_number(self, serverid):
        async with aiosqlite.connect('utilities/databases/tickets.db') as db:
            db.row_factory = aiosqlite.Row
            sql = f'SELECT * FROM servers WHERE serverid = ?'
            cursor = await db.execute(sql, (serverid,))
            cursor = await cursor.fetchone()

            return cursor['tickets']

    async def set_message_id(self, id, message_id, server_id):
        async with aiosqlite.connect('utilities/databases/tickets.db') as db:
            sql = f'UPDATE server_{server_id} SET message_id = ? WHERE id = ?'
            cursor = await db.execute(sql, (message_id, id,))
            await db.commit()

    async def set_info_id(self, id, message_id, server_id):
        async with aiosqlite.connect('utilities/databases/tickets.db') as db:
            sql = f'UPDATE server_{server_id} SET info_message_id = ? WHERE id = ?'
            cursor = await db.execute(sql, (message_id, id,))
            await db.commit()

    async def set_log_channel(self, server_id, channel_id):
        async with aiosqlite.connect('utilities/databases/tickets.db') as db:
            sql = f'UPDATE servers SET log_channel = ? WHERE serverid = ?'
            await db.execute(sql, (channel_id, server_id,))
            await db.commit()

    async def delete_ticket(self, guild, ticket):
        async with aiosqlite.connect('utilities/databases/tickets.db') as db:
            sql = f'DELETE FROM server_{guild} WHERE id = ?'
            cursor = await db.execute(sql, (ticket))
            await db.commit()


class QuickCommands:
    async def add_qc(self, cmd, response):
        async with aiosqlite.connect('utilities/databases/cmds.db') as db:
            sql = f'INSERT INTO qc (command, response) VALUES (?, ?)'
            cursor = await db.execute(sql, (cmd, response,))
            await db.commit()
            return cursor.lastrowid

    async def del_qc(self, id):
        async with aiosqlite.connect('utilities/databases/cmds.db') as db:
            sql = f'DELETE FROM qc WHERE id = ?'
            await db.execute(sql, (id,))
            await db.commit()

    async def edit_qc(self, id, new_response):
        async with aiosqlite.connect('utilities/databases/cmds.db') as db:
            sql = f'UPDATE qc SET response = ? WHERE id = ?'
            await db.execute(sql, (id, new_response,))
            await db.commit()

    async def get_qc_by_id(self, id):
        async with aiosqlite.connect('utilities/databases/cmds.db') as db:
            db.row_factory = aiosqlite.Row
            sql = f'SELECT * FROM qc WHERE id = ?'
            cursor = await db.execute(sql, (id,))
            cursor = await cursor.fetchone()
            return cursor

    async def get_qc_by_cmd(self, cmd):
        async with aiosqlite.connect('utilities/databases/cmds.db') as db:
            db.row_factory = aiosqlite.Row
            sql = f'SELECT * FROM qc WHERE command = ?'
            cursor = await db.execute(sql, (cmd,))
            cursor = await cursor.fetchone()
            return cursor

    async def get_all_cmds(self):
        async with aiosqlite.connect('utilities/databases/cmds.db') as db:
            db.row_factory = aiosqlite.Row
            sql = f'SELECT * FROM qc'
            cursor = await db.execute(sql)
            cursor = await cursor.fetchall()
            return cursor
