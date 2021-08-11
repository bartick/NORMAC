import datetime
import discord
from discord.ext import commands
import traceback
import humanize
import sys

class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.application_ids = {
            "YOUTUBE": [755600276941176913, "Watch Youtube Go"],
            'POKER': [755827207812677713, "Play Poker Night"],
            'BETRAYAL': [773336526917861400, "Play Betrayal.io"],
            'FISHING': [814288819477020702, "Play Fishington.io"],
            'CHESS': [832012774040141894, "Play Chess In The Park"]
        }
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return
        
        ignored = (commands.CommandNotFound, discord.Forbidden, commands.NotOwner, discord.HTTPException, discord.NotFound)

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return
        
        if isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except Exception:
                pass
        
        elif isinstance(error, commands.BotMissingPermissions):
            try:
                await ctx.send("Bot is missing required `Create Instant Invite` permission to run this command")
            except Exception:
                pass
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'Retry after {humanize.precisedelta(datetime.timedelta(seconds=error.retry_after),minimum_unit="seconds")}...')

        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
    
    async def post_invite(self, ctx: commands.Context, key:str):

        voice_state = ctx.author.voice
        if voice_state==None:
            await ctx.send("You need to be in a vc to use this command")
            return

        invite = await voice_state.channel.create_invite(
            max_age=86400,
            target_type=discord.InviteTarget.embedded_application,
            target_application_id=self.application_ids[key][0]
        )
        
        view = discord.ui.View(timeout=1)
        view.add_item(discord.ui.Button(label=f"Join Activity", url=invite.url))
        embed = discord.Embed(color=0x2F3136)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.timestamp = datetime.datetime.now()
        embed.title = self.application_ids[key][1]
        embed.description = "Click the url button below to join the activity.\n\n**Note:** According to my knowledge this only works on pc. If you want to complain I can't help because this is a limitation imposed by discord.\nThank You."

        await ctx.send(content=ctx.author.mention, embed=embed, view=view)
    
    @commands.command(
        name="youtube",
        help="Starts a embeded youtube application",
        aliases=['yt']
    )
    @commands.guild_only()
    @commands.bot_has_permissions(create_instant_invite=True)
    async def youtube(self, ctx):
        await self.post_invite(ctx, "YOUTUBE")
    
    @commands.command(
        name="poker",
        help="Play Poker Night in your server",
        aliases=['pn']
    )
    @commands.guild_only()
    @commands.bot_has_permissions(create_instant_invite=True)
    async def poker(self, ctx):
        await self.post_invite(ctx, "POKER")
    
    @commands.command(
        name="chess",
        help="Play Chess In The Park in your server",
        aliases=['citp']
    )
    @commands.bot_has_permissions(create_instant_invite=True)
    @commands.guild_only()
    async def chess(self, ctx):
        await self.post_invite(ctx, "CHESS")
    
    @commands.command(
        name="betrayal",
        help="Play betrayal.io in your server",
        aliases=["bio"]
    )
    @commands.bot_has_permissions(create_instant_invite=True)
    @commands.guild_only()
    async def betrayal(self, ctx):
        await self.post_invite(ctx, "BETRAYAL")

    @commands.command(
        name="fishing",
        help="Play Fishington.io in your server",
        aliases=['fio']
    )
    @commands.bot_has_permissions(create_instant_invite=True)
    @commands.guild_only()
    async def fishing(self, ctx):
        await self.post_invite(ctx, "FISHING")
    
    @commands.command()
    @commands.guild_only()
    async def invite(self, ctx):
        await ctx.send(f"To invite me to your server use the link below.\nhttps://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=84993&scope=bot")


def setup(bot):
    bot.add_cog(Main(bot))