import discord
from discord.ext import commands
import asyncio

class WebcomicCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    from .webcomics.twokinds import twokinds

def setup(client):
    client.add_cog(WebcomicCommands(client))
