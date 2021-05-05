import os
import discord
import logging
from discord.ext import commands
from datetime import datetime
import json

os.system("")

with open("cfg.json") as f:
	c = json.load(f)

def get_prefix(bot,msg):
	if not str(msg.guild.id) in c:
		cfg=c["default"]
	else:
		cfg=c[str(msg.guild.id)]

	allcfg=c["all"]

	return commands.when_mentioned_or(*(cfg["prefixes"]),*(allcfg["prefixes"]))(bot, msg)

intents = discord.Intents.all()
client = commands.Bot(
	description="Positively Lewd Hentai God",
	activity=discord.Activity(
		name="Hentai",
		type=discord.ActivityType.watching
		),
	intents=intents,
	command_prefix=get_prefix
)
client.remove_command('help')


time = datetime.now()
date = datetime.now()
formatTime = time.strftime("%H:%M:%S")
formatDate = time.strftime("%d/%m/%Y")

logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="vawbot.log", encoding="utf-8")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)


@client.event
async def on_ready():
	print("\u001b[32m" + "HENTAI FOR ALL @ " + formatTime + " on the " + formatDate + "\u001b[37m")

@client.command()
@commands.is_owner()
async def load(ctx, extension):
	client.load_extension(f"cogs.{extension}")

	embed = discord.Embed(
		title="Bot Management",
		description=f"Successfully loaded the following cog: {extension.upper()}",
		colour=discord.Colour.green()
	)

	print("\u001b[33m" + f"Loaded the following cog: {extension.upper()}" + "\u001b[37m")
	await ctx.send(embed=embed)


@client.command()
@commands.is_owner()
async def unload(ctx, extension):
	client.unload_extension(f"cogs.{extension}")

	embed = discord.Embed(
		title="Bot Management",
		description=f"Successfully unloaded the following cog: {extension.upper()}",
		colour=discord.Colour.green()
	)

	print("\u001b[33m" + f"Unloaded the following cog: {extension.upper()}" + "\u001b[37m")
	await ctx.send(embed=embed)


@client.command()
@commands.is_owner()
async def reload(ctx, extension):
	client.unload_extension(f"cogs.{extension}")
	client.load_extension(f"cogs.{extension}")

	embed = discord.Embed(
		title="Bot Management",
		description=f"Successfully reloaded the following cog: {extension.upper()}",
		colour=discord.Colour.green()
	)

	print("\u001b[33m" + f"Reloaded the following cog: {extension.upper()}" + "\u001b[37m")
	await ctx.send(embed=embed)


@client.command()
@commands.is_owner()
async def loglevel(ctx, *, level="info"):
	levels = {
		"critical": logging.CRITICAL,
		"error": logging.ERROR,
		"warn": logging.WARNING,
		"warning": logging.WARNING,
		"info": logging.INFO,
		"debug": logging.DEBUG
	}

	logger.setLevel(levels[level])

	embed = discord.Embed(
		title="Bot Management",
		description=f"Log level set to: {level.upper()}",
		colour=discord.Colour.green()
	)

	print("\u001b[33m" + f"Log level set to: {level.upper()}" + "\u001b[37m")
	await ctx.send(embed=embed)

for filename in os.listdir("cogs"):
	if filename.endswith(".py"):
		client.load_extension(f"cogs.{filename[:-3]}")

tokens = open("tokens.txt", "r").readlines()
client.run(tokens[0])
