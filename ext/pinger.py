import json

import aiohttp
from discord.ext import commands, tasks


class Pinger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._ticker.start()

    # Task every 25 seconds to change channel name
    @tasks.loop(seconds=25.0)
    async def _ticker(self):
        params = {'api_key': "29u2q98dhq2dq'2qd09q2u3d#2qdq209hdj", 'id': '5'}
        try:
            async with aiohttp.ClientSession() as session:
                resp = await session.get('https://hazzakak.tech/api/v1.0/ping', params=params)
                data = await resp.read()
                data = json.loads(data)
                print(f"Response: {'OK' if data['response'] == 200 else 'ERROR'}")
        except:
            return print("Error with pinger, retrying in 25 seconds.")

    @_ticker.before_loop
    async def before_printer(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Pinger(bot))
