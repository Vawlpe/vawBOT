import discord
from discord.ext import commands

from datetime import datetime
import os

#TOKEN = open("token.txt").read() #LOCAL TESTING
TOKEN = os.getenv('TOKEN')

client = commands.Bot(
	command_prefix = "vaw.",
	description="Positively Lewd Hentai God",
	activity=discord.Activity(
		name="Hentai",
		type=discord.ActivityType.watching
		)
	)

@client.event
async def on_ready():
    print("HENTAI FOR ALL")


# Here we load our cogs
if __name__ == '__main__':
	for f in os.listdir("cogs"):
		if f.endswith('.py'):
			client.load_extension(f'cogs.{f.replace(".py","")}')

client.run(TOKEN)
