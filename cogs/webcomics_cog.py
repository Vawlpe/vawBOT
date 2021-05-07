import discord
from discord.ext import commands
import asyncio
import json

class comics(commands.Cog):
    def __init__(self, client):
        self.client = client

    def cog_check(self, ctx):
        with open("cfg.json") as f:
            c = json.load(f)

        if not str(ctx.guild.id) in c:
            cfg=c["default"]
        else:
            cfg=c[str(ctx.guild.id)]

        allcfg=c["all"]

        # Some of this logic may be redundant but i got rly confused so i just wrote a truth table and converted it to a K-map
        return (not "comics" in cfg["cog_blacklist"] and not "comics" in allcfg["cog_blacklist"]) or (
            not "comics" in cfg["cog_blacklist"] and "comics" in cfg["cog_whitelist"])


    from .webcomics.twokinds import twokinds

def setup(client):
    client.add_cog(comics(client))
