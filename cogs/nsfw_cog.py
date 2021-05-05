import discord
from discord.ext import commands
import asyncio
import json

# Cogs setup bs
class nsfw(commands.Cog):
	def __init__(self, client):
		self.client = client

	from .nsfw.nhentai import nhv, nhr
	from .nsfw.luscious import lctest
	from .nsfw.nekos_life import nl
	from .nsfw.nekos_moe import nm

	def cog_check(self, ctx):
		with open("cfg.json") as f:
			c = json.load(f)

		if not str(ctx.guild.id) in c:
			cfg=c["default"]
		else:
			cfg=c[str(ctx.guild.id)]

		allcfg=c["all"]

		# Some of this logic may be redundant but i got rly confused so i just wrote a truth table and converted it to a K-map
		return (ctx.channel.is_nsfw() and not "nsfw" in cfg["cog_blacklist"] and not "nsfw" in allcfg["cog_blacklist"]) or (
			ctx.channel.is_nsfw() and not "nsfw" in cfg["cog_blacklist"] and "nsfw" in cfg["cog_whitelist"])

# More cogs setup bs
def setup(client):
	client.add_cog(nsfw(client))
