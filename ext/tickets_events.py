import asyncio
import datetime
import logging
import os

import discord
from discord.ext import commands

from config import Config
from utilities.database import Tickets

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class TicketsEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, g):
        await Tickets().add_server(g.id)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, r):
        guild = self.bot.get_guild(r.guild_id)
        user = self.bot.get_user(r.user_id)
        channel = self.bot.get_channel(r.channel_id)

        # Check if its a stop emoji
        if str(r.emoji) == u"\U0001F6D1":
            # Check if it's been done by the bot
            if r.user_id != self.bot.user.id:
                await self.bot.http.remove_reaction(r.channel_id, r.message_id, r.emoji, r.user_id)
            else:
                return

            if "ticket" not in channel.name:
                return

            log_channel = await Tickets().get_log_channel(guild.id)

            if log_channel[0] == None:
                embed = discord.Embed(title=f"{Config(self.bot).name} (V{Config(self.bot).version})",
                                      color=discord.Colour.blue())
                embed.set_author(name="JBot", icon_url="https://hazzakak.tech/images/P6V7B32Y.png")
                embed.description = f"Log channel has not been set, management can set this with `*log-channel [channel mention]`, this ticket will delete in 30 seconds without saving."
                await channel.send(embed=embed)

                await asyncio.sleep(30)
                return await channel.delete()

            embed = discord.Embed(title=f"{Config(self.bot).name} (V{Config(self.bot).version})",
                                  color=discord.Colour.blue())
            embed.set_author(name="JBot", icon_url="https://hazzakak.tech/images/P6V7B32Y.png")
            embed.description = f"Logging transcript."
            await channel.send(embed=embed)

            log_channel = guild.get_channel(int(log_channel[0]))

            channel_name = channel.name.replace(" ", "_") + ".html"

            with open("utilities/format.html", 'r', encoding='utf-8') as test:
                file = test.read()

            with open(channel_name, "w+") as a:
                body = ""
                async for m in channel.history(limit=None, oldest_first=True):
                    body += str(
                        f"""<div class="box"><h2 style="color:#d6d6d6;">{m.author.name}#{m.author.discriminator}<span class="time">{m.created_at.strftime('%Y-%m-%d %H:%M:%S')}</span></h2><p style="color:#dcddde;">{m.content}</p></div>""")
                a.write(file)
            with open(channel_name, "r") as b:
                replace_string = b.read()
                replace_1 = replace_string.replace("{{channel}}", channel.name)
                replace_2 = replace_1.replace("{{placeholder}}", body)
            with open(channel_name, "w") as c:
                c.write(replace_2)

            embed = discord.Embed(
                title=f'Audit Log',
                colour=discord.Colour.blue(),
                timestamp=datetime.datetime.utcnow(),
                description=f"`User:` {user.name}#{user.discriminator}\n`Action:` Closed Ticket"
            )

            await log_channel.send(embed=embed, file=discord.File(channel_name))
            os.remove(channel_name)
            await channel.delete()

            return

        tickets = await Tickets().get_tickets(guild.id)

        # Checks if there is any tickets to listen to
        if len(tickets) == 0:
            return

        for t in tickets:
            # Checks if the message id is the same as the one usd in setup
            if int(t['message_id']) == r.message_id:
                # make sure it is the same emoji
                if str(r.emoji) != u"\U0001F516":
                    return

                # deletes emoji if user is not a bot.
                if r.user_id != self.bot.user.id:
                    await self.bot.http.remove_reaction(r.channel_id, r.message_id, r.emoji, r.user_id)
                else:
                    return

                await Tickets().add_ticket_number(guild.id)
                ticket_number = await Tickets().get_ticket_number(guild.id)
                invCat = discord.utils.get(self.bot.get_guild(r.guild_id).categories, id=channel.category_id)

                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    guild.me: discord.PermissionOverwrite(read_messages=True),
                    guild.get_member(r.user_id): discord.PermissionOverwrite(read_messages=True)
                }

                roles = t['roles'].split('.')
                for role in roles:
                    if role == '':
                        continue
                    dict1 = {guild.get_role(int(role)): discord.PermissionOverwrite(read_messages=True)}
                    overwrites.update(dict1)

                perpChannel = await guild.create_text_channel(name=f"ticket-{ticket_number}", category=invCat,
                                                              overwrites=overwrites)
                message = await perpChannel.send(t['info_message'])
                await Tickets().set_info_id(t['id'], message.id, guild.id)
                await message.add_reaction(u"\U0001F6D1")


def setup(bot):
    bot.add_cog(TicketsEvents(bot))
