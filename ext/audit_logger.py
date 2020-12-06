import datetime

import discord
from discord.ext import commands, tasks

from utilities.database import Tickets


class AuditLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.audit_check.start()

    @tasks.loop(seconds=3.0)
    async def audit_check(self):
        for guild in self.bot.guilds:
            channel_id = await Tickets().get_log_channel(guild.id)
            if channel_id[0] is None:
                continue
            audit = guild.get_channel(int(channel_id[0]))
            async for entry in guild.audit_logs(oldest_first=True):
                if entry.created_at >= datetime.datetime.utcnow() - datetime.timedelta(seconds=3):
                    if entry.action is discord.AuditLogAction.ban:
                        embed = discord.Embed(
                            title=f'Audit Log',
                            colour=discord.Colour.red(),
                            timestamp=entry.created_at,
                            description=f"`User:` {entry.user.name}#{entry.user.discriminator}\n`Action:` Banned\n`Target:` {entry.target}\n`Reason:` {entry.reason}"
                        )
                        return await audit.send(embed=embed)
                    if entry.action is discord.AuditLogAction.kick:
                        embed = discord.Embed(
                            title=f'Audit Log',
                            colour=discord.Colour.red(),
                            timestamp=entry.created_at,
                            description=f"`User:` {entry.user.name}#{entry.user.discriminator}\n`Action:` Kicked\n`Target:` {entry.target}\n`Reason:` {entry.reason}"
                        )
                        await audit.send(embed=embed)
                    if entry.action is discord.AuditLogAction.channel_create:
                        embed = discord.Embed(
                            title=f'Audit Log',
                            colour=discord.Colour.blue(),
                            timestamp=entry.created_at,
                            description=f"`User:` {entry.user.name}#{entry.user.discriminator}\n`Action:` Created Channel\n`Channel:` {entry.target.mention}"
                        )
                        return await audit.send(embed=embed)

                    if entry.action is discord.AuditLogAction.channel_delete:
                        embed = discord.Embed(
                            title=f'Audit Log',
                            colour=discord.Colour.red(),
                            timestamp=entry.created_at,
                            description=f"`User:` {entry.user.name}#{entry.user.discriminator}\n`Action:` Deleted Channel"
                        )
                        return await audit.send(embed=embed)

                    if entry.action is discord.AuditLogAction.channel_update:
                        embed = discord.Embed(
                            title=f'Audit Log',
                            colour=discord.Colour.red(),
                            timestamp=entry.created_at,
                            description=f"`User:` {entry.user.name}#{entry.user.discriminator}\n`Action:` Edited Channel\n`Channel:` {entry.target.mention}"
                        )
                        return await audit.send(embed=embed)

                    if entry.action is discord.AuditLogAction.unban:
                        embed = discord.Embed(
                            title=f'Audit Log',
                            colour=discord.Colour.red(),
                            timestamp=entry.created_at,
                            description=f"`User:` {entry.user.name}#{entry.user.discriminator}\n`Action:` Unbanned\n`Target:` {entry.target}\n`Reason:` {entry.reason}"
                        )
                        return await audit.send(embed=embed)

                    if entry.action is discord.AuditLogAction.member_role_update:
                        embed = discord.Embed(
                            title=f'Audit Log',
                            colour=discord.Colour.green(),
                            timestamp=entry.created_at,
                            description=f"`User:` {entry.user.name}#{entry.user.discriminator}\n`Action:` Updated Roles\n`Target:` {entry.target}"
                        )
                        return await audit.send(embed=embed)
                    if entry.action is discord.AuditLogAction.role_update:
                        embed = discord.Embed(
                            title=f'Audit Log',
                            colour=discord.Colour.green(),
                            timestamp=entry.created_at,
                            description=f"`User:` {entry.user.name}#{entry.user.discriminator}\n`Action:` Updated Role\n`Target:` {entry.target}"
                        )
                        return await audit.send(embed=embed)
                    if entry.action is discord.AuditLogAction.role_create:
                        embed = discord.Embed(
                            title=f'Audit Log',
                            colour=discord.Colour.green(),
                            timestamp=entry.created_at,
                            description=f"`User:` {entry.user.name}#{entry.user.discriminator}\n`Action:` Created Role\n`Role:` {entry.target.mention}"
                        )
                        return await audit.send(embed=embed)
                    if entry.action is discord.AuditLogAction.role_delete:
                        embed = discord.Embed(
                            title=f'Audit Log',
                            colour=discord.Colour.red(),
                            timestamp=entry.created_at,
                            description=f"`User:` {entry.user.name}#{entry.user.discriminator}\n`Action:` Deleted Role\n`Role:` {entry.target.mention}"
                        )
                        return await audit.send(embed=embed)
                    if entry.action is discord.AuditLogAction.overwrite_update or entry.action is discord.AuditLogAction.overwrite_create:
                        embed = discord.Embed(
                            title=f'Audit Log',
                            colour=discord.Colour.red(),
                            timestamp=entry.created_at,
                            description=f"`User:` {entry.user.name}#{entry.user.discriminator}\n`Action:` Updated Permissions\n`Target:` {entry.target.mention if entry.target is discord.TextChannel else entry.target.name}"
                        )
                        return await audit.send(embed=embed)
                    if entry.action is discord.AuditLogAction.overwrite_update or entry.action is discord.AuditLogAction.message_pin:
                        embed = discord.Embed(
                            title=f'Audit Log',
                            colour=discord.Colour.red(),
                            timestamp=entry.created_at,
                            description=f"`User:` {entry.user.name}#{entry.user.discriminator}\n`Action:` Pinned Message\n`Pinned Message:` {entry.extra.message_id}\n`Channel:` {entry.extra.channel.mention}"
                        )
                        return await audit.send(embed=embed)

                    embed = discord.Embed(
                        title=f'Audit Log',
                        colour=discord.Colour.green(),
                        timestamp=entry.created_at,
                        description=f"`User:` {entry.user.name}#{entry.user.discriminator}\n`Action:` {entry.action}\n`Target:` {entry.target}\n`Reason:` {entry.reason}"
                    )
                    await audit.send(embed=embed)

    @audit_check.before_loop
    async def before_printer(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(AuditLogger(bot))
