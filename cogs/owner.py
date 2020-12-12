import discord
from discord.ext import commands
import requests


class AdminCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    # Hidden means it won't show up on the default help.
    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def mod_load(self, ctx, *, cog: str):
        """Command which Loads a Module."""

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def mod_unload(self, ctx, *, cog: str):
        """Command which Unloads a Module."""

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def mod_reload(self, ctx, *, cog: str):
        """Command which Reloads a Module."""

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='dm', hidden=True)
    @commands.is_owner()
    async def dm(ctx, member : discord.Member, *, text):
        await ctx.send(text)
        
    @commands.command(name='exitserver', hidden=True)
    @commands.is_owner()
    async def exitserver(self, ctx):
        await ctx.send("ok bye")
        guild = ctx.guild
        await guild.leave()

    @commands.command(name='bonkhorny')
    @commands.has_permissions(manage_channels=True)
    @commands.is_owner()
    async def bonkhorny(self, ctx, channel: discord.TextChannel, role: discord.Role):
        url = 'https://api.jsonbin.io/v3/b/5fd40dd1fbb23c2e36a5a16c'
        old = requests.get(url+"/latest").json()['record']
        data = old + [{
            "channel": f"{channel.id}",
            "role": f"{role.id}",
            "users": {}
            }]
        requests.put(url, json=data, headers={'Content-Type': 'application/json'})
            
def setup(bot):
    bot.add_cog(AdminCommands(bot))
