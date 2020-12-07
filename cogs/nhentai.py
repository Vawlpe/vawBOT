import discord
from discord.ext import commands
import asyncio

from hentai import Hentai, Format, Utils

# Helper funcs
async def viewDoujin(self, ctx, d):
    # Create Embed...
    embed=discord.Embed(color=0x850054, 
                        title=d.title(Format.Pretty),
                        url=d.url,
                        description=f"Artists: {', '.join(artist.name for artist in d.artist)}\nTags: {', '.join(tag.name for tag in d.tag)}")
    embed.set_thumbnail(url='https://i.imgur.com/uLAimaY.png')
    embed.set_image(url=d.cover)
    embed.add_field(name='Read',value=':book: REACT BELLOW')
    embed.add_field(name='Download',value=f'[:inbox_tray: Torrent](https://nhentai.net/login/?next=%2Fg%2F{d.id}%2Fdownload)')
    embed.add_field(name='Favorite',value=f'[:star: {d.num_favorites}](https://nhentai.net/login/?next=%2Fg%2F{d.id}%2F)')
    embed.set_footer(text=f'ID: {d.id} | {d.num_pages} Pages')

    #Send and add reaction button
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("📖")

    # Added reaction Check callback
    def check(reaction, user):
        isSameMsg = reaction.message == msg 
        read = reaction.emoji == '📖'
        notBot = reaction.count>1 and reaction.me
        isSameUser = (usr async for usr in reaction.users() if usr == msg.author)
        return isSameMsg and read and notBot and isSameUser

    # Wait for user to react and redirect them to NHREAD
    try:
        await self.client.wait_for('reaction_add', timeout=120.0, check=check)
    except asyncio.TimeoutError:
        print(f'NHVIEW {d.id} Read Reaction Timeout')
    else:
        print(f'NHVIEW {d.id} -> NHREAD')
        await ctx.send("Redirecting to NHREAD...")
        await self.client.get_cog('NHCog').nhr(ctx, id=d.id, replaceMsg=msg)

# Cogs setup bs
class NHCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    # NHVIEW
    @commands.command()
    async def nhv(self, ctx, *, id=''):
        print(f'NHView {id}...')

        # Doujin exists?
        if Hentai.exists(id):
                d = Hentai(id)
                print(f'NHVIEW {id} found')
                await viewDoujin(self, ctx, d)
        # No ID? Send random
        elif not id:
            print(f'NHVIEW No ID; Sending random')
            await ctx.send('No ID passed, getting random doujin...')
            await viewDoujin(self, ctx, Utils.get_random_hentai())
        # ID not digits
        elif not id.isdigit():
            print(f'NHVIEW Invalid ID')
            await ctx.send('Invalid ID\nIDs are usually 6 digit numbers, although there are some 5 digin and even shorter or longer IDs\nIf you don\'t have an ID just don\'t write one and we will send you a random doujin :3')
        else:
            print(f'NHVIEW {id} not found ;-;')
            await ctx.send(f'No Doujin with id: {id} was found\nIf you don\'t have an ID just don\'t write one and we will send you a random doujin :3')

    # NHREAD
    @commands.command()
    async def nhr(self, ctx, *, id, replaceMsg):
        print('NHREAD... WIP ;-;')
        await ctx.send('NHREAD (nhr) Command has not been implemented yet')

# More cogs setup bs
def setup(client):
    client.add_cog(NHCog(client))
