import discord
from discord.ext import commands

from datetime import datetime
import requests
import os

#TOKEN = open("token.txt").read() #LOCAL TESTING
TOKEN = os.getenv('TOKEN') # Heroku

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

@client.event
async def on_message(message):
	if not message.author.id == client.user.id:
		url = 'https://api.jsonbin.io/v3/b/5fd40dd1fbb23c2e36a5a16c/latest'
		old = requests.get(url).json()['record']
		for c in old:
			if c["channel"] == f'{message.channel.id}':
				if not message.guild.get_role((int(c["role"]))) in message.author.roles:
					await message.author.add_roles(discord.Object(id=c["role"]))
					embed = discord.Embed(color=0x81B4D6, title=f"WELCOME TO HORNY JAIL YOU FILTHY SCUM", description=f"{message.author.mention}")
					embed.set_image(url="https://i.kym-cdn.com/entries/icons/original/000/033/758/Screen_Shot_2020-04-28_at_12.21.48_PM.png")
					await message.channel.send(embed=embed)
					data = old
					data[data.index(c)] = {"channel":f'{c["channel"]}', "role":f'{c["role"]}'}
					requests.put(url, json=data, headers={'Content-Type': 'application/json'})

	await client.process_commands(message)

@client.command()
async def ping(ctx):
	await ctx.send(f'Pong! {int(client.latency*1000)}ms')


# Here we load our cogs
if __name__ == '__main__':
	for f in os.listdir("cogs"):
		if f.endswith('.py'):
			client.load_extension(f'cogs.{f.replace(".py","")}')

client.run(TOKEN)
