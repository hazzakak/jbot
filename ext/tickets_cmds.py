import logging

import discord
from discord.ext import commands

from utilities.database import Tickets

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class TicketsCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="add-ticket", aliases=['add_ticket', 'at'])
    @commands.guild_only()
    async def add_ticket(self, ctx):
        """
        Creates a ticket category where the 'setup-tickets' can be used to list the support ticket.
        """

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.send("What is the ticket called?")
        ticket_name = await self.bot.wait_for('message', check=check)

        await ctx.send("Who can view this ticket? *tag all the roles you want to be able to see it*")
        ticket_roles = await self.bot.wait_for('message', check=check)

        await ctx.send("What message should be sent upon the opening of the ticket?")
        ticket_info_message = await self.bot.wait_for('message', check=check)

        roles = ""
        for role in ticket_roles.role_mentions:
            roles += f"{role.id}."

        database_query = await Tickets().add_tickets(roles, ticket_name.content, ctx.guild.id,
                                                     ticket_info_message.content)
        await ctx.send(
            f"Added ticket, use `{ctx.prefix}setup-tickets`. If you made a mistake use `{ctx.prefix}delete-ticket {database_query}`")

    @commands.command(name="view-tickets", aliases=['view_tickets', 'vt'])
    @commands.guild_only()
    async def view_tickets(self, ctx):
        """
        View all of the guilds tickets.
        """
        tickets = await Tickets().get_tickets(ctx.guild.id)

        embed = discord.Embed(
            title='Tickets',
            colour=discord.Colour.blue()
        )
        embed.set_author(name='Ticket Bot')

        desc = ""
        for t in tickets:
            desc += f"ID: `{t['id']}`\nName: `{t['name']}`\n\n"

        embed.description = desc
        await ctx.send(embed=embed)

    @commands.command(name="setup-tickets")
    @commands.guild_only()
    async def channel_setup(self, ctx):
        """
        This lists all the tickets for the guild and adds a reaction for it to be activated.
        """
        tickets = await Tickets().get_tickets(ctx.guild.id)

        for t in tickets:
            embed = discord.Embed(title=f"{t['name']}",
                                  color=discord.Colour.blue())
            embed.description = f"To create a ticket hit the :bookmark: reaction."
            embed.set_author(name="JBot", icon_url="https://hazzakak.tech/images/P6V7B32Y.png")
            message = await ctx.send(embed=embed)

            await Tickets().set_message_id(t['id'], message.id, ctx.guild.id)

            await message.add_reaction(u"\U0001F516")

    @commands.command(name="del-ticket", aliases=['delete-ticket'])
    @commands.guild_only()
    async def del_ticket(self, ctx, id: int):
        """
        Deletes ticket based on the id, found in 'view-tickets'.
        """
        await Tickets().delete_ticket(ctx.guild.id, id)
        return await ctx.send("Ticket has been deleted")


def setup(bot):
    bot.add_cog(TicketsCmds(bot))
