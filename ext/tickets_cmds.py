import discord
from discord.ext import commands

from utilities.database import Ticket


class TicketCommands(commands.Cog, name="Ticket Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(manage_guild=True)
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

        database_query = await Ticket().add_ticket_group(ticket_name.content, roles, ticket_info_message.content,
                                                         ctx.guild.id)
        await ctx.send(
            f"Added ticket, use `{ctx.prefix}setup-tickets`. If you made a mistake use `{ctx.prefix}delete-ticket {database_query}`")

    @commands.has_permissions(manage_guild=True)
    @commands.command(name="view-tickets", aliases=['view_tickets', 'vt'])
    @commands.guild_only()
    async def view_tickets(self, ctx):
        """
        View all of the guilds tickets.
        """

        tickets = await Ticket().get_all_ticket_groups(ctx.guild.id)

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

    @commands.has_permissions(manage_guild=True)
    @commands.command(name="setup-tickets")
    @commands.guild_only()
    async def channel_setup(self, ctx):
        """
        This lists all the tickets for the guild and adds a reaction for it to be activated.
        """

        tickets = await Ticket().get_all_ticket_groups(ctx.guild.id)

        for t in tickets:
            embed = discord.Embed(title=f"{t['name']}",
                                  color=discord.Colour.blue())
            embed.description = f"To create a ticket hit the :bookmark: reaction."
            embed.set_author(name="JBot", icon_url="https://hazzakak.tech/i/P6V7B32Y.png")
            message = await ctx.send(embed=embed)

            await Ticket().update_ticket_group(t['id'], message.id)

            await message.add_reaction(u"\U0001F516")

    @commands.has_permissions(manage_guild=True)
    @commands.command(name="del-ticket", aliases=['delete-ticket'])
    @commands.guild_only()
    async def del_ticket(self, ctx, id: int):
        """
        Deletes ticket based on the id, found in 'view-tickets'.
        """
        if ctx.guild.id not in [640322944408748042, 754728584165458060, 759519145708224553, 344620042836639744]:
            return

        await Ticket().del_ticket_group(id)
        return await ctx.send("Ticket has been deleted")


def setup(bot):
    bot.add_cog(TicketCommands(bot))
