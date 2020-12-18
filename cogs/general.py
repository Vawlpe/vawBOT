import discord
from discord.ext import commands
import asyncio


class GeneralCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
	    await ctx.send(f'Pong! {int(self.client.latency*1000)}ms')


def setup(client):
    client.add_cog(GeneralCommands(client))