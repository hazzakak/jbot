from discord.ext import commands

from utilities.database import ReactRoles


class ReactRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="react-list-add", aliases=['rla', 'react-add'])
    async def _add_list(self, ctx, name):
        db = ReactRoles()

        if await db.get_list_by_name(name):
            return await ctx.send("That list already exists.")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        roles_list = []
        response = ""

        await ctx.send("Mention each role below in a new message, when finished type `stop`.")

        while response != 'stop':
            roles = await self.bot.wait_for('message', check=check)
            response = roles.content

            if response == 'stop':
                continue

            if len(roles.role_mentions) != 1:
                return await ctx.send("Only one role can be selected per reaction")

            roles_list.append([roles.role_mentions[0].id])
            await ctx.send(f"Added {roles.role_mentions[0].mention}")

        await ctx.send("React to each role below with which emoji it should be associated with.")

        for r in roles_list:
            role = ctx.guild.get_role(r[0])
            reaction_message = await ctx.send(f"{role.mention}")

            def check(reaction, user):
                return not user.bot and reaction.message.id == reaction_message.id and user.id == ctx.author.id

            reaction, user = await self.bot.wait_for('reaction_add', check=check)
            r.append(str(reaction.emoji))
            continue

        await db.add_list(name, roles_list, ctx.guild.id)
        await ctx.send(f"Role react list has been setup, use `{ctx.prefix}react-list-setup {name}` to enable the list.")

    @commands.command(name="react-list-setup", aliases=['rls', 'react-setup'])
    async def _setup_list(self, ctx, name):
        db = ReactRoles()
        role_list = await db.get_list_by_name(name)

        if not role_list:
            return await ctx.send(f"List does not exist, use `{ctx.prefix}react-list-add <name>`.")

        msg = await ctx.send("React to get the respective role.\n")

        for r in eval(role_list['roles']):
            role = ctx.guild.get_role(r[0])
            await msg.edit(content=f"{msg.content}\n{role.mention} - {r[1]}")
            await msg.add_reaction(r[1])

        await db.update_message_id(name, msg.id)


def setup(bot):
    bot.add_cog(ReactRole(bot))
