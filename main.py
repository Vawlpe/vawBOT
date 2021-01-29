from datetime import datetime
import requests
import os

import discord
from discord.ext import commands
from pretty_help import PrettyHelp

TOKEN = open("../token.txt").read() #LOCAL TXT FILE
#TOKEN = os.getenv('TOKEN') # ENV VAR	

client = commands.Bot(
	command_prefix = "vaw.",
	description="Positively Lewd Hentai God",
	help_command=PrettyHelp(active_time=180),
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
