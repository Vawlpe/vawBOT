import discord
from discord.ext import commands
import asyncio
import json


class general(commands.Cog):
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
		return (not "general" in cfg["cog_blacklist"] and not "general" in allcfg["cog_blacklist"]) or (
			not "general" in cfg["cog_blacklist"] and "general" in cfg["cog_whitelist"])

	@commands.command()
	async def ping(self, ctx):
		await ctx.send(f'Pong! {int(self.client.latency*1000)}ms')

	@commands.command()
	# @commands.bot_has_permissions(add_reactions=True,embed_links=True)
	async def help(self, ctx, *input):
		"""Shows all modules of the bot"""
		prefix = await self.client.get_prefix(ctx.message)

		# checks if cog parameter was given
		# if not: sending all modules and commands not associated with a cog
		if not input:

			# starting to build embed
			emb = discord.Embed(title='Commands and modules', color=discord.Color.blue(),
								description=f'Use `{prefix}help <module>` to gain more hot sticky- i mean >.> \"information\" about that command')

			# iterating trough cogs, gathering descriptions
			cogs_desc = ''
			for name,cog in self.client.cogs.items():
				if cog.cog_check(ctx):
					cogs_desc += f'`{name}` {self.client.cogs[name].__doc__}\n'

			# adding 'list' of cogs to embed
			emb.add_field(name='Modules', value=cogs_desc, inline=False)

			# integrating trough uncategorized commands
			commands_desc = ''
			for command in self.client.walk_commands():
				# if cog not in a cog
				# listing command if cog name is None and command isn't hidden
				if not command.cog_name and not command.hidden:
					commands_desc += f'{command.name} - {command.help}\n'

			# adding those commands to embed
			if commands_desc:
				emb.add_field(name='Not belonging to a module', value=commands_desc, inline=False)

		# block called when one cog-name is given
		# trying to find matching cog and it's commands
		elif len(input) == 1:

			# iterating trough cogs
			for cog in self.client.cogs:
				# check if cog is the matching one
				if cog.cog_check(self,ctx) and cog.lower() == input[0].lower():

					# making title - getting description from doc-string below class
					emb = discord.Embed(title=f'{cog} - Commands', description=self.client.cogs[cog].__doc__,
										color=discord.Color.green())

					# getting commands from cog
					for command in self.client.get_cog(cog).get_commands():
						# if cog is not hidden
						if not command.hidden:
							emb.add_field(name=f"`{prefix}{command.name}`", value=command.help, inline=False)
					# found cog - breaking loop
					break

			# if input not found
			# yes, for-loops have an else statement, it's called when no 'break' was issued
			else:
				emb = discord.Embed(title="UwU What's this?!",
									description=f"I've never heard of a module called `{input[0]}` before :pleading_face:",
									color=discord.Color.red())

		# too many cogs requested - only one at a time allowed
		elif len(input) > 1:
			emb = discord.Embed(title="OwO thats a lot of ~~cocks~~ cogs",
								description="Please only request one module at once :hot_face:",
								color=discord.Color.red())

		else:
			emb = discord.Embed(title="WTF....",
								description="How did you even get here...",
								color=discord.Color.red())

		# sending reply embed using our own function defined above
		await ctx.send(embed=emb)


def setup(client):
	client.add_cog(general(client))
