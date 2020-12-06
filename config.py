import json
import logging
import traceback

import discord

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class Roles:
    def __init__(self):
        self.management = "--------- Management ---------"
        self.moderator = "Moderator"

    def get_management_role(self):
        return self.management

    def get_moderator_role(self):
        return self.moderator


class Config:
    def __init__(self, bot):
        self.name = "JBot"
        self.version = "3.0.0"
        self.bot = bot
        self.extensions: list = ['tickets_cmds', 'tickets_events', 'error_handler', 'listener', 'moderation',
                                 'help_command', 'info', 'audit_logger', 'pinger', 'react_role']
        self.all_roles = [694477201839620157, 631218469974573077, 694476941188923392, 631218097122181161,
                          694476941188923392, 631218035318849538, 681917448072462470, 681916937701556257,
                          631218229854863373, 694477201839620157, 631218229854863373]
        self.management = "--------- Management ---------"
        self.moderator = "Moderator"
        self.log_channel = 742660198673416223
        self.welcome_channel = 742662564101750826

    def embed(self, color=discord.Colour.blue()):
        embed = discord.Embed(color=color)
        embed.set_author(name="JBot", icon_url='https://hazzakak.tech/i/P6V7B32Y.png')

        return embed

    def get_token(self):
        with open('token.json') as token:
            data = json.load(token)
            return data['token']

    def get_management_role(self):
        return self.management

    def get_moderator_role(self):
        return self.moderator

    def load_cogs(self):
        try:
            print("=======- Loading Extensions -======")
            for x in self.extensions:
                try:
                    x = 'ext.' + x
                    self.bot.load_extension(x)
                    print('Loaded: {0}'.format(x))
                except Exception as e:
                    traceback.print_exc()
                    print('Could not load: {0}'.format(x))
            print("=======-   Loaded Extensions  -======\n\n")
        except:
            return 'Error'

    def get_usual_roles(self):
        category_role = self.bot.guilds[0].get_role(694477201839620157)
        usual_role = self.bot.guilds[0].get_role(631218469974573077)

        return category_role, usual_role

    def get_dev_roles(self):
        category_role = self.bot.guilds[0].get_role(694476941188923392)
        dev_role = self.bot.guilds[0].get_role(631218097122181161)

        return [category_role, dev_role]

    def get_mod_roles(self):
        category_role = self.bot.guilds[0].get_role(694476941188923392)
        mod_role = self.bot.guilds[0].get_role(631218035318849538)

        return [category_role, mod_role]

    def get_friend_roles(self):
        category_role = self.bot.guilds[0].get_role(694477201839620157)
        friend_role = self.bot.guilds[0].get_role(631218229854863373)

        return [category_role, friend_role]
