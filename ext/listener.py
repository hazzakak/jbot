import asyncio
import datetime
import os

import discord
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from discord.ext import commands

from config import Config
from utilities.database import ReactRoles


class EventListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_image(self, member):
        in_file = 'images/' + 'background.png'

        x = 20
        y = 20

        img = Image.open(in_file)

        draw = ImageDraw.Draw(img)

        text = f"Welcome\n{member.name}#{member.discriminator}\nTo JBot Server"
        shadowcolor = 'black'

        font = ImageFont.truetype("utilities/font/ariblk.ttf", 100)

        # left welcome message
        draw.text((x - 3, y - 3), text, font=font, fill=shadowcolor)
        draw.text((x + 3, y - 3), text, font=font, fill=shadowcolor)
        draw.text((x - 3, y + 3), text, font=font, fill=shadowcolor)
        draw.text((x + 3, y + 3), text, font=font, fill=shadowcolor)

        draw.text((x, y), text, fill='white', font=font)

        img.save('images/' + str(member.id) + '.png')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, r):
        guild = self.bot.get_guild(r.guild_id)
        user = guild.get_member(r.user_id)

        db = ReactRoles()
        react_list = await db.get_list_by_msg(r.message_id)

        if not react_list:
            return

        for x in eval(react_list['roles']):
            if x[1] == str(r.emoji):
                role = guild.get_role(x[0])
                await user.add_roles(role)
            else:
                pass

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, r):
        guild = self.bot.get_guild(r.guild_id)
        user = guild.get_member(r.user_id)

        db = ReactRoles()
        react_list = await db.get_list_by_msg(r.message_id)

        if not react_list:
            return

        for x in eval(react_list['roles']):
            if x[1] == str(r.emoji):
                role = guild.get_role(x[0])
                await user.remove_roles(role)
            else:
                pass

    @commands.Cog.listener()
    async def on_ready(self):
        app_info = await self.bot.application_info()

        print(f'Discord bot ({app_info.name}) is ready.')
        print(f'Bot latency: {round(self.bot.latency * 100, 3)}ms\n\n')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        config = Config(self.bot)
        audit = member.guild.get_channel(config.log_channel)

        embed = discord.Embed(
            title=f'Audit Log',
            colour=discord.Colour.red(),
            timestamp=datetime.datetime.now(),
            description=f"`User:` {member.name}#{member.discriminator} ({member.id})\n`Action:` Left Server"
        )
        return await audit.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        roles = Config(self.bot).get_usual_roles()
        config = Config(self.bot)

        for r in roles:
            await member.add_roles(r)
        print(f"{member.name} has been given starting roles.")

        # Log the enterance in log channel
        embed = config.embed()

        join_embed = discord.Embed(
            title=f'Audit Log',
            colour=discord.Colour.red(),
            timestamp=datetime.datetime.now(),
            description=f"`User:` {member.name}#{member.discriminator} ({member.mention})\n`Action:` Joined Server"
        )

        log_channel = member.guild.get_channel(config.log_channel)
        await log_channel.send(embed=join_embed)

        # Log the enterance in welcome channel
        await self.get_image(member)
        await asyncio.sleep(2)
        file = discord.File(f'images/{member.id}.png', filename=f'{member.id}.png')

        embed.set_image(url=f'attachment://{member.id}.png')

        welcome_channel = member.guild.get_channel(config.welcome_channel)
        await welcome_channel.send(file=file, embed=embed)
        os.remove(f'images/{member.id}.png')


def setup(bot):
    bot.add_cog(EventListener(bot))
