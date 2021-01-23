import asyncio
import logging
import os

import discord
from discord.ext import commands

from config import Config
from utilities.database import Ticket

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class TicketsEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, r):
        guild = self.bot.get_guild(r.guild_id)
        user = self.bot.get_user(r.user_id)
        channel = self.bot.get_channel(r.channel_id)

        if type(channel) == discord.channel.DMChannel:
            return

        # Check if it's been done by the bot
        if r.user_id == self.bot.user.id:
            return

        if str(r.emoji) == "🔖":
            tickets = await Ticket().get_all_ticket_groups(guild.id)
            for t in tickets:
                if int(t['message']) == r.message_id:
                    await self.bot.http.remove_reaction(r.channel_id, r.message_id, r.emoji, r.user_id)
                    invCat = discord.utils.get(self.bot.get_guild(r.guild_id).categories,
                                               id=756207113205710941 if guild.id is 754728584165458060 else channel.category.id)

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
                    ticket_numb = await Ticket().get_ticket_number(guild.id)

                    channel = await guild.create_text_channel(name=f"ticket-{ticket_numb}", category=invCat,
                                                              overwrites=overwrites)
                    await Ticket().update_ticket_number(guild.id)
                    message = await channel.send(t['description'])
                    await Ticket().add_ticket(message.id)
                    await message.add_reaction("🔒")
                    await message.add_reaction("➕")
                    await message.add_reaction("➖")
            return

        get_ticket = await Ticket().get_ticket_by_id(r.message_id)

        # check if its a ticket channel
        if get_ticket is None:
            return

        # removes reaction
        await self.bot.http.remove_reaction(r.channel_id, r.message_id, r.emoji, r.user_id)

        if str(r.emoji) == "🔒":
            log_channel = await Ticket().get_log_channel(guild.id)
            tickets = await Ticket().get_tickets()

            if log_channel is None:
                embed = discord.Embed(title=f"{Config(self.bot).name} (V{Config(self.bot).version})",
                                      color=discord.Colour.blue())
                embed.set_author(name="JBot", icon_url="https://hazzakak.tech/i/P6V7B32Y.png")
                embed.description = f"Log channel has not been set, management can set this with `!s log-channel [channel mention]`, this ticket will delete in 15 seconds without saving."
                await channel.send(embed=embed)

                await asyncio.sleep(15)
                return await channel.delete()

            embed = discord.Embed(title=f"{Config(self.bot).name} (V{Config(self.bot).version})",
                                  color=discord.Colour.blue())
            embed.set_author(name="JBot", icon_url="https://hazzakak.tech/i/P6V7B32Y.png")
            embed.description = f"Logging transcript."
            await channel.send(embed=embed)

            log_channel_obj = guild.get_channel(int(log_channel))

            channel_name = channel.name.replace(" ", "_") + ".html"

            with open("utilities/format.html", 'r', encoding='utf-8') as test:
                file = test.read()

            members = []
            members_str = ""

            with open(channel_name, "w+") as a:
                body = ""
                async for m in channel.history(limit=None, oldest_first=True):
                    if m.author not in members:
                        members_str += f"{m.author.mention}\n"
                        members.append(m.author)
                    body += str(
                        f"""<div class="box"><h2 style="color:#d6d6d6;">{m.author.name}#{m.author.discriminator}<span class="time">{m.created_at.strftime('%Y-%m-%d %H:%M:%S')}</span></h2><p style="color:#dcddde;">{m.content}</p></div>""")
                a.write(file)
            with open(channel_name, "r") as b:
                replace_string = b.read()
                replace_1 = replace_string.replace("{{channel}}", channel.name)
                replace_2 = replace_1.replace("{{placeholder}}", body)
            with open(channel_name, "w") as c:
                c.write(replace_2)

            embed.add_field(name="Ticket Name", value=channel.name)
            embed.add_field(name="Ticket Members", value=members_str)
            embed.add_field(name="Channel", value=channel.mention)
            await log_channel_obj.send(embed=embed, file=discord.File(channel_name))
            os.remove(channel_name)
            await asyncio.sleep(3)
            return await channel.delete()
        elif str(r.emoji) == "➕":
            def check(m):
                return m.author == user and m.channel == channel

            # activates a prompt asking who to add to the chat
            await channel.send("What user do you want to add (type 'stop' if you want to exit)?")
            user_to_add = await self.bot.wait_for('message', check=check)

            if user_to_add.content == "stop":
                await channel.send("Stopped.")
                return

            # upon answering: add the player
            for m in user_to_add.mentions:
                await channel.set_permissions(m, read_messages=True, send_messages=True)
            await channel.send("User(s) have been added,")
            return
        elif str(r.emoji) == "➖":
            def check(m):
                return m.author == user and m.channel == channel

            # activates a prompt asking who to remove from the chat
            await channel.send("What user do you want to remove (type 'stop' if you want to exit)?")
            user_to_add = await self.bot.wait_for('message', check=check)

            if user_to_add.content == "stop":
                await channel.send("Stopped.")
                return

            # upon answering: remove the player
            for m in user_to_add.mentions:
                await channel.set_permissions(m, read_messages=False, send_messages=False)
            await channel.send("User(s) have been removed.")
            return


def setup(bot):
    bot.add_cog(TicketsEvents(bot))
