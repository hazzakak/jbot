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


class Ticket:
    # add a ticket to the database
    async def add_ticket_group(self, name, viewroles, description, guild):
        async with aiosqlite.connect('utilities/databases/tickets.db') as db:
            sql = f'INSERT INTO ticket_groups (name, guild, description, roles) VALUES (?, ?, ?, ?)'
            cursor = await db.execute(sql, (name, guild, description, viewroles,))
            await db.commit()
            return cursor.lastrowid

    # delete a ticket from teh database
    async def del_ticket_group(self, id):
        async with aiosqlite.connect('utilities/databases/tickets.db') as db:
            sql = f'DELETE FROM ticket_groups WHERE id = ?'
            await db.execute(sql, (id,))
            await db.commit()

    # update the ticket's message to add the message id
    async def update_ticket_group(self, id, message):
        async with aiosqlite.connect('utilities/databases/tickets.db') as db:
            sql = f'UPDATE ticket_groups SET message = ? WHERE id = ?'
            await db.execute(sql, (message, id,))
            await db.commit()

    # get all ticket groups
    async def get_all_ticket_groups(self, guild):
        async with aiosqlite.connect('utilities/databases/tickets.db') as db:
            db.row_factory = aiosqlite.Row
            sql = f'SELECT * FROM ticket_groups WHERE guild = ?'
            cursor = await db.execute(sql, (guild,))
            return await cursor.fetchall()

    async def get_log_channel(self, guild):
        async with aiosqlite.connect('utilities/databases/tickets.db') as db:
            db.row_factory = aiosqlite.Row
            sql = f'SELECT * FROM server WHERE serverid = ?'
            cursor = await db.execute(sql, (guild,))
            cursor = await cursor.fetchone()
            return cursor['channel']

    # add an individual ticket to the database
    async def add_ticket(self, message_id):
        async with aiosqlite.connect('utilities/databases/tickets.db') as db:
            sql = f'INSERT INTO tickets (message) VALUES (?)'
            await db.execute(sql, (message_id,))
            await db.commit()

    async def del_ticket(self, message_id):
        async with aiosqlite.connect('utilities/databases/tickets.db') as db:
            sql = f'DELETE FROM tickets WHERE message = ?'
            await db.execute(sql, (message_id,))
            await db.commit()

    async def get_ticket_by_id(self, message):
        async with aiosqlite.connect('utilities/databases/tickets.db') as db:
            db.row_factory = aiosqlite.Row
            sql = f'SELECT * FROM tickets WHERE message = ?'
            cursor = await db.execute(sql, (message,))
            return await cursor.fetchone()

    async def get_tickets(self):
        async with aiosqlite.connect('utilities/databases/tickets.db') as db:
            db.row_factory = aiosqlite.Row
            sql = f'SELECT * FROM tickets'
            cursor = await db.execute(sql)
            return await cursor.fetchall()

    async def get_ticket_number(self, guild):
        async with aiosqlite.connect('utilities/databases/tickets.db') as db:
            db.row_factory = aiosqlite.Row
            sql = f'SELECT * FROM server WHERE serverid = ?'
            cursor = await db.execute(sql, (guild,))
            cursor = await cursor.fetchone()
            return cursor['ticket']

    async def update_ticket_number(self, guild):
        async with aiosqlite.connect('utilities/databases/tickets.db') as db:
            sql = f'UPDATE server SET ticket = ticket+1 WHERE serverid = ?'
            await db.execute(sql, (guild,))
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
