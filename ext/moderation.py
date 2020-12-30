import discord
from discord.ext import commands

from config import Config, Roles


class ModerationCommands(commands.Cog, name="Moderation Commands"):
    def __init__(self, bot):
        self.bot = bot

    async def usual_rank(self, member):
        roles = Config(self.bot).get_usual_roles()
        for r in roles:
            await member.add_roles(r)

    async def developer_rank(self, member):
        roles = Config(self.bot).get_dev_roles()
        for r in roles:
            await member.add_roles(r)

    async def moderator_rank(self, member):
        roles = Config(self.bot).get_mod_roles()
        for r in roles:
            await member.add_roles(r)

    async def friend_rank(self, member):
        roles = Config(self.bot).get_friend_roles()
        for r in roles:
            await member.add_roles(r)

    async def remove_roles(self, user, ctx):
        for r in user.roles:
            if r.id in Config(self.bot).all_roles:
                await user.remove_roles(ctx.guild.get_role(r.id))
        return True

    @commands.has_role(Roles().management)
    @commands.command(name="changerank", aliases=['cr'])
    @commands.guild_only()
    async def _changerank(self, ctx, user: discord.Member, *, level):
        """
        Changes the discord rank of a user, removes other rank roles and adds the new one. Visitor, Friend, Developer, or Moderator.
        """

        level = level.lower()

        if level == 'visitor':
            await self.remove_roles(user, ctx)
            await self.usual_rank(user)
            embed = Config(self.bot).embed()
            embed.description = f"{user.mention}'s level has been changed to {level}"
            embed.set_author(name="JBot", icon_url="https://hazzakak.tech/images/P6V7B32Y.png")

            return await ctx.send(embed=embed)
        if level == 'developer':
            await self.remove_roles(user, ctx)
            await self.developer_rank(user)
            embed = Config(self.bot).embed()

            embed.description = f"{user.mention}'s level has been changed to {level}"
            embed.set_author(name="JBot", icon_url="https://hazzakak.tech/images/P6V7B32Y.png")

            return await ctx.send(embed=embed)
        if level == 'moderator':
            await self.remove_roles(user, ctx)
            await self.moderator_rank(user)
            embed = Config(self.bot).embed()
            embed.description = f"{user.mention}'s level has been changed to {level}"
            embed.set_author(name="JBot", icon_url="https://hazzakak.tech/images/P6V7B32Y.png")

            return await ctx.send(embed=embed)
        if level == 'friend':
            await self.remove_roles(user, ctx)
            await self.friend_rank(user)
            embed = Config(self.bot).embed()
            embed.description = f"{user.mention}'s level has been changed to {level}"
            embed.set_author(name="JBot", icon_url="https://hazzakak.tech/images/P6V7B32Y.png")

            return await ctx.send(embed=embed)

        embed = Config(self.bot).embed()
        embed.set_author(name="JBot", icon_url="https://hazzakak.tech/images/P6V7B32Y.png")
        embed.description = f"Incorrect level parameter"
        return await ctx.send(embed=embed)

    @commands.has_role(Roles().moderator)
    @commands.command()
    @commands.guild_only()
    async def clear(self, ctx, amount: int = 2):
        """
        Clears the amount of messages specified above the command.
        """
        loading_msg = await ctx.send(content=f"Deleting {amount} messages.")

        def check(m):
            return m.id != loading_msg.id

        await ctx.channel.purge(limit=amount, check=check)
        await loading_msg.edit(content=f"{amount} messages have been deleted.")

    '''@commands.has_role(Roles().management)
    @commands.command(name="changelog", aliases=['cl'])
    @commands.guild_only()
    async def _changelog(self, ctx, channel: discord.TextChannel):
        """
        Changes the log channel which audit logs and transcripts are sent to.
        """
        await Tickets().set_log_channel(ctx.guild.id, channel.id)

        embed = Config(self.bot).embed()
        embed.set_author(name="JBot", icon_url="https://hazzakak.tech/images/P6V7B32Y.png")
        embed.description = f"Log channel has been changed to {channel.mention}"
        return await ctx.send(embed=embed)'''


def setup(bot):
    bot.add_cog(ModerationCommands(bot))
