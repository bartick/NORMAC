from discord.ext import commands, tasks
import aiohttp

class TopGG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.post_count.start()

    @tasks.loop(seconds=3600)
    async def post_count(self):
        if self.bot.topToken==None:
            self.post_count.stop()
            return
        url = f"https://top.gg/api/bots/{self.bot.user.id}/stats"
        data = {
            "server_count": len(self.bot.guilds)
        }
        headers = {
            "Authorization": self.bot.topToken
        }
        async with aiohttp.ClientSession(loop=self.bot.loop) as session:
            await session.post(url=url, data=data, headers=headers)
    
    @post_count.before_loop
    async def before_post_count(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(TopGG(bot))