import discord
from discord.ext import commands, menus
import asyncio

from hentai import Hentai, Format, Utils
import nekos

# Menus
class viewDoujinMenu(menus.Menu):
    async def start(self, ctx, d):
        self.d = d
        await super().start(ctx)

    async def send_initial_message(self, ctx, channel):
        # Create Embed...
        embed=discord.Embed(color=0xE12754, 
            title=self.d.title(Format.Pretty),
            url=self.d.url
        )
        embed.set_thumbnail(url='https://i.imgur.com/uLAimaY.png') # NH Logo
        embed.set_image(url=self.d.cover)

        if self.d.artist: embed.add_field(name='Artist',value=f"{', '.join(artist.name for artist in self.d.artist)}")
        if self.d.language: embed.add_field(name='Language',value=f"{', '.join(lang.name for lang in self.d.language)}")
        if self.d.group: embed.add_field(name='Group',value=f"{', '.join(group.name for group in self.d.group)}")
        if self.d.parody: embed.add_field(name='Parody',value=f"{', '.join(parody.name for parody in self.d.parody)}")
        if self.d.category: embed.add_field(name='Category',value=f"{', '.join(cat.name for cat in self.d.category)}")
        if self.d.character: embed.add_field(name='Characters',value=f"{', '.join(char.name for char in self.d.character)}")
        if self.d.tag: embed.add_field(name='Tags',value=f"{', '.join(tag.name for tag in self.d.tag)}",inline=False)

        embed.add_field(name='Read',value=':book: React To Read')
        embed.add_field(name='Download',value=f'[:inbox_tray: Torrent](https://nhentai.net/login/?next=%2Fg%2F{self.d.id}%2Fdownload)')
        embed.add_field(name='Favorite',value=f'[:star: {self.d.num_favorites}](https://nhentai.net/login/?next=%2Fg%2F{self.d.id}%2F)')
        embed.set_footer(text=f'ID: {self.d.id} | {self.d.num_pages} Pages')

        return await ctx.send(embed=embed)

    @menus.button('\N{OPEN BOOK}')
    async def on_book_open(self, payload):
        await viewPageMenu().start(self.ctx, self.d)
        await self.message.delete()
        self.stop()

class viewPageMenu(menus.Menu):
    async def start(self, ctx, d):
        self.d=d
        self.page=0
        await super().start(ctx)

    async def domsg(self, ctx=None):
        # Create Embed...
        embed=discord.Embed(color=0xE12754, 
            title=self.d.title(Format.Pretty),
            url=self.d.url
        )
        embed.set_thumbnail(url='https://i.imgur.com/uLAimaY.png') # NH Logo
        embed.set_image(url=self.d.image_urls[self.page])
        embed.add_field(name='Download',value=f'[:inbox_tray: Torrent](https://nhentai.net/login/?next=%2Fg%2F{self.d.id}%2Fdownload)')
        embed.add_field(name='Favorite',value=f'[:star: {self.d.num_favorites}](https://nhentai.net/login/?next=%2Fg%2F{self.d.id}%2F)')
        embed.set_footer(text=f'ID: {self.d.id} | {self.page+1}/{self.d.num_pages} Pages')
        if self.message is None:
            return await ctx.send(embed=embed)
        else:
            await self.message.edit(embed=embed)

    async def send_initial_message(self, ctx, channel):
        return await self.domsg(ctx)

    @menus.button('⏮️')
    async def on_start(self, payload):
        self.page=0
        await self.domsg()

    @menus.button('⬅️')
    async def on_prev(self, payload):
        self.page=max(0, min(self.page-1, self.d.num_pages-1))
        await self.domsg()

    @menus.button('➡️')
    async def on_next(self, payload):
        self.page=max(0, min(self.page+1, self.d.num_pages-1))
        await self.domsg()

    @menus.button('⏭️')
    async def on_end(self, payload):
        self.page=self.d.num_pages-1
        await self.domsg()



# Cogs setup bs
class HentaiCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    # NSFW
    def cog_check(self, ctx):
        return ctx.channel.is_nsfw()
        
    # NHView
    @commands.command()
    async def nhv(self, ctx, *, id=None):
        print(f'NHView {id}...')

        # Doujin exists?
        if Hentai.exists(id):
                d = Hentai(id)
                print(f'NHVIEW {id} found')
                await viewDoujinMenu().start(ctx, d)
        # No ID? Send random
        elif id is None:
            print(f'NHVIEW No ID; Sending random')
            await ctx.send('No ID passed, getting random doujin...')
            await viewDoujinMenu().start(ctx, Utils.get_random_hentai())
        # ID not digits
        elif not id.isdigit():
            print(f'NHVIEW Invalid ID')
            await ctx.send('Invalid ID\nIDs are usually 6 digit numbers, although there are some 5 digin and even shorter or longer IDs\nIf you don\'t have an ID just don\'t write one and we will send you a random doujin :3')
        else:
            print(f'NHVIEW {id} not found ;-;')
            await ctx.send(f'No Doujin with id: {id} was found\nIf you don\'t have an ID just don\'t write one and we will send you a random doujin :3')

    # NHRead
    @commands.command()
    async def nhr(self, ctx, *, id=None):
        print(f'NHREAD {id}...')

        # Doujin exists?
        if Hentai.exists(id):
                d = Hentai(id)
                print(f'NHREAD {id} found')
                await viewPageMenu().start(ctx, d)
        # No ID? Send random
        elif id is None:
            print(f'NHREAD No ID; Sending random')
            await ctx.send('No ID passed, getting random doujin...')
            await viewPageMenu().start(ctx, Utils.get_random_hentai())
        # ID not digits
        elif not id.isdigit():
            print(f'NHREAD Invalid ID')
            await ctx.send('Invalid ID\nIDs are usually 6 digit numbers, although there are some 5 digin and even shorter or longer IDs\nIf you don\'t have an ID just don\'t write one and we will send you a random doujin :3')
        else:
            print(f'NHREAD {id} not found ;-;')
            await ctx.send(f'No Doujin with id: {id} was found\nIf you don\'t have an ID just don\'t write one and we will send you a random doujin :3')

    # NekosLife
    @commands.command()
    async def nl(self, ctx, *, tag):
        print(f'NekosLife {tag}...')
        pic = nekos.img(tag)

        # Create Embed...
        embed=discord.Embed(color=0xC54EAD, 
            title=tag,
            url=pic
        )
        embed.set_thumbnail(url='https://nekos.life/static/icons/favicon-194x194.png') # Nekos.life Logo
        embed.set_image(url=pic)
        embed.set_footer(text=f'nekos.life: {tag}')
        await ctx.send(embed=embed)

# More cogs setup bs
def setup(client):
    client.add_cog(HentaiCommands(client))
