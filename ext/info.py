import discord
from discord.ext import commands

from config import Config


class InformationCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="guild")
    async def _guildinformation(self, ctx):
        # Information
        guild = ctx.guild
        name = guild.name
        icon = guild.icon_url
        description = guild.description
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        members = guild.members
        members_amount = len(members)
        bots = [x for x in members if x.bot]
        owner = guild.owner
        created_at = guild.created_at

        # Defining the embed
        embed = Config(self.bot).embed()
        embed.set_author(name="JBot", icon_url="https://hazzakak.tech/images/P6V7B32Y.png")

        embed.description = '*No guild set description*' if description is None else description

        embed.add_field(name="Members", value=f"Members: {members_amount - len(bots)}\nBots: {len(bots)}")
        embed.add_field(name="Channels", value=f"Text Channels: {text_channels}\nVoice Channels: {voice_channels}")
        embed.add_field(name="Stats",
                        value=f"ID: {guild.id}\nOwner: {owner.mention}\nCreated at: {str(created_at)[:-7]}",
                        inline=False)

        return await ctx.send(embed=embed)

    @commands.command(name="player")
    async def _playerinformation(self, ctx, player: discord.Member = None):
        """
        Gets current information about a player.
        """

        # Player equals author if player argument is not specified.
        player = ctx.author if player is None else player

        # Defining the embed
        embed = discord.Embed(title="DankusBotus", color=discord.Colour.blue())
        embed.set_thumbnail(url=player.avatar_url)

        # Gathering information
        player_id = player.id
        player_joined = player.joined_at
        player_nick = player.display_name
        player_status = player.status
        player_roles = player.roles
        player_joined_discord = player.created_at

        status_emoji = [[discord.Status.online, u"\U0001F7E2"], [discord.Status.offline, u"\U000026ab"],
                        [discord.Status.idle, u"\U0001f7e0"], [discord.Status.dnd, u"\U0001f534"]]
        for i, x in status_emoji:
            if i == player_status:
                status_emoji = x
            else:
                continue
        embed.description = f"""**ID:** {player_id}
        **Username:** {player_nick}
        **Status:** {status_emoji} {str(player_status).capitalize()}

        **Joined Guild:** {player_joined}
        **Joined Discord:** {player_joined_discord}

        **Roles:**
        {[i.mention for i in player_roles]}
        """

        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(InformationCommands(bot))
