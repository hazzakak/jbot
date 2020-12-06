import logging

import discord
from discord.ext import commands

from config import Config

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(
    command_prefix='!',
    case_insensitive=True,
    description="Created by harry#3275.",
    activity=discord.Activity(type=discord.ActivityType.listening, name="the cries"),
    help_command=None
)

if __name__ == '__main__':
    Config(bot).load_cogs()

bot.run(Config(bot).get_token())
