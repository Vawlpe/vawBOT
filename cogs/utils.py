import discord
from discord.ext import commands
import asyncio

# I WANT TO DIE
class UtilsCog(commands.Cog):
	def __init__(self, client):
		self.client = client

	expectedReactions = []

	async def expectMsgReactions(self, msg, reaction, callback):
		self.expectedReactions.append([msg, reaction, callback])

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		for entry in self.expectedReactions:
			if entry[0].id == payload.message_id and entry[1] == payload.emoji.name and payload.user_id != self.client.user.id and discord.utils.get(discord.utils.get(await entry[0].channel.history(limit=100).flatten(), id=entry[0].id).reactions, emoji=entry[1]).count>1:
				await entry[2]()

def setup(client):
    client.add_cog(UtilsCog(client))