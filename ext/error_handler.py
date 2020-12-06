import sys
import traceback

import discord
from discord.ext import commands

from config import Config


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Embed definition
        embed = Config(self.bot).embed(color=discord.Color.red())
        app_info = await self.bot.application_info()

        error = getattr(error, 'original', error)

        # Prevent unknown commands and incorrect user input to return anything.
        if isinstance(error, commands.CommandNotFound):
            embed.description = f"The command `{ctx.invoked_with}` does not exist."
            return await ctx.send(embed=embed)
        elif isinstance(error, commands.DisabledCommand):
            embed.description = f"The command `{ctx.command}` has been disabled."
            return await ctx.send(embed=embed)
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                embed.description = f"The command `{ctx.command} cannot be used in a private message."
                return await ctx.send(embed=embed)
            except:
                pass
        elif isinstance(error, commands.MissingPermissions):
            embed.description = f"You do not have permission to use `{ctx.command}`."
            return await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed.description = f"Incorrect arguments. Use `{ctx.prefix}help {ctx.command}` to find help."
            return await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed.description = f"Incorrect arguments. Use `{ctx.prefix}help {ctx.command}` to find help."
            return await ctx.send(embed=embed)
        elif isinstance(error, commands.TooManyArguments):
            embed.description = f"Incorrect arguments. Use `{ctx.prefix}help {ctx.command}` to find help."
            return await ctx.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed.description = f"{app_info.name} is missing the required permissions."
            return await ctx.send(embed=embed)

        # All other Errors not returned come here... And we can just print the default TraceBack.
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
