import math

from discord.ext import commands

from config import Config


class HelpCommand(commands.Cog, name="Help Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def help(self, ctx, page='none'):
        """
        Get a list of commands and their usage to help your use of the bot.
        """
        if page is 'none':
            page = 1
        try:
            page = int(page)
        except:
            page = page

        if type(page) is int:
            body = ''

            for x in self.bot.cogs:
                for y in self.bot.get_cog(x).get_commands():
                    cog_name = y.cog_name
                    if cog_name is None:
                        cog_name = "Main"
                    body += f"Usage: {ctx.prefix}{y.name} {y.signature}\nCategory: {cog_name}\nDescription: {y.help}\n"
            pages = int(math.ceil(len(body) / 975))
            paginator = commands.Paginator(prefix="```autohotkey\n",
                                           suffix=f"\nPage {page}/{pages}, use {ctx.prefix}help [page] to find other pages.```",
                                           max_size=1050)

            for x in self.bot.cogs:
                for y in self.bot.get_cog(x).get_commands():
                    cog_name = y.cog_name
                    if cog_name is None:
                        cog_name = "Main"
                    paginator.add_line(
                        f"Usage: {ctx.prefix}{y.name} {y.signature}\nCategory: {cog_name}\nDescription: {y.help}\n")

            pages = len(paginator.pages)
            if int(page) > int(pages):
                return await ctx.send(f"There's only {pages} pages.")

            page_1 = page - 1

            for o, p in enumerate(paginator.pages):
                if o == page_1:
                    await ctx.send(p)
        else:
            command = self.bot.get_command(page)
            if command is None:
                embed = Config(self.bot).embed()
                embed.description = f"That command doesn't exist."
                return await ctx.send(embed=embed)
            embed = Config(self.bot).embed()
            embed.description = f"{command.help}\nUsage: `{ctx.prefix}{command} {command.signature}`"
            return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(HelpCommand(bot))
