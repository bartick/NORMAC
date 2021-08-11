import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import environ, listdir
import traceback

load_dotenv()

class MyBot(commands.Bot):
    def __init__(self, **options):
        self.prefix = "."
        self.token = options.pop("token",None)
        super().__init__(command_prefix=self.prefix, **options)
    
    async def on_ready(self):
        print(f"Logged in as {self.user}")
    
    def load_cogs(self):
        print("Loading Cog")
        for file in listdir('cogs'):
            if file.endswith(".py"):
                try:
                    self.load_extension(f"cogs.{file[:-3]}")
                except Exception:
                    traceback.print_exc()
                else:
                    print(f"Loaded {file[:-3]}")
    
    def start_bot(self):
        self.load_cogs()
        self.run(self.token)

intents = discord.Intents.default()

kwargs = {
    "intents": intents,
    "case_insensitive": True,
    "token": environ.get("TOKEN"),
    "activity": discord.Game(name="looking into discord Embeded Games"),
    "description": "**A Discord Embeded Application Bot.**"
}

bot = MyBot(**kwargs)

if __name__=='__main__':
    bot.start_bot()