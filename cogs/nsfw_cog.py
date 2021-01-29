import discord
from discord.ext import commands
import asyncio

# Cogs setup bs
class HentaiCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    from .nsfw.nhentai import nhv, nhr
    from .nsfw.luscious import lctest
    from .nsfw.nekos_life import nl
    from .nsfw.nekos_moe import nm, nmsafe, nmlewd

    async def cog_check(self, ctx):
        return ctx.channel.is_nsfw()

# More cogs setup bs
def setup(client):
    client.add_cog(HentaiCommands(client))