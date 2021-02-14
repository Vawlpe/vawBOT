import discord
from discord.ext import commands
import requests

class AdminCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)
    
    # Hidden means it won't show up on the default help.
    @commands.command(name='load', hidden=True)
    async def mod_load(self, ctx, *, cog: str):
        """Command which Loads a Module."""
        embed = discord.Embed(title="Extension Management",color=0xFF0000)

        try:
            self.bot.load_extension(f'cogs.{cog}')
        except Exception as e:
            embed.description=f'Error trying to load {cog}:\n{type(e).__name__} - {e}'
        else:
            embed.color=0x00FF00
            embed.description=f'Successfuly loaded {cog}'

        await ctx.send(embed=embed)

    @commands.command(name='unload', hidden=True)
    async def mod_unload(self, ctx, *, cog: str):
        """Command which Unloads a Module."""
        embed = discord.Embed(title="Extension Management",color=0xFF0000)

        try:
            self.bot.unload_extension(f'cogs.{cog}')
        except Exception as e:
            embed.description=f'Error trying to unload {cog}:\n{type(e).__name__} - {e}'
        else:
            embed.color=0x00FF00
            embed.description=f'Successfuly unloaded {cog}'

        await ctx.send(embed=embed)


    @commands.command(name='reload', hidden=True)
    async def mod_reload(self, ctx, *, cog: str):
        """Command which Reloads a Module."""
        embed = discord.Embed(title="Extension Management",color=0xFF0000)

        try:
            self.bot.unload_extension(f'cogs.{cog}')
            self.bot.load_extension(f'cogs.{cog}')
        except Exception as e:
            embed.description=f'Error trying to reload {cog}:\n{type(e).__name__} - {e}'
        else:
            embed.color=0x00FF00
            embed.description=f'Successfuly reloaded {cog}'
        
    @commands.command(name='exitserver', hidden=True)
    async def exitserver(self, ctx):
        await ctx.send("ok bye")
        await ctx.guild.leave()

def setup(bot):
    bot.add_cog(AdminCommands(bot))