import discord
from discord.ext import commands, menus
import asyncio

from hentai import Hentai, Format, Utils

import menus.read as readmenu
import menus.view as viewmenu

# NHRead
@commands.command()
async def nhr(self, ctx, *, id=None):
    print(f'NHREAD {id}...')

    # No ID? Send random
    if id is None:
        print(f'NHREAD No ID; Sending random')
        await ctx.send('No ID passed, getting random doujin...')
        d = Utils.get_random_hentai()
    # ID not digits
    elif not id.isdigit():
        print(f'NHREAD Invalid ID')
        await ctx.send('Invalid ID\nIDs are usually 6 digit numbers, although there are some 5 digin and even shorter or longer IDs\nIf you don\'t have an ID just don\'t write one and we will send you a random doujin :3')
    # Does Doujin exist?
    elif Hentai.exists(id):
        d = Hentai(id)
        print(f'NHREAD {id} found')
    else:
        print(f'NHREAD {id} not found ;-;')
        await ctx.send(f'No Doujin with id: {id} was found\nIf you don\'t have an ID just don\'t write one and we will send you a random doujin :3')

    info={
        'title':d.title(Format.Pretty),
        'url':d.url,
        'color':0xE12754,
        'thumbnail':'https://i.imgur.com/uLAimaY.png',
        'page':1,
        'footerFormat':'{other}{page}/{total_pages}',
        'footerExtra':f'ID: {d.id} | ',
        'extra_fields':[
            {'name':'Download','value':f'[:inbox_tray: Torrent](https://nhentai.net/login/?next=%2Fg%2F{d.id}%2Fdownload)'},
            {'name':'Favorite','value':f'[:star: {d.num_favorites}](https://nhentai.net/login/?next=%2Fg%2F{d.id}%2F)'}
        ],
        'imgURLs':d.image_urls,
        'showbtns':[True,False,True]*2
    }

    return await readmenu.ReadMenu().start(ctx, **info)


# NHView
@commands.command()
async def nhv(self, ctx, *, id=None):
    print(f'NHView {id}...')

    # No ID? Send random
    if id is None:
        print(f'NHVIEW No ID; Sending random')
        await ctx.send('No ID passed, getting random doujin...')
        d=Utils.get_random_hentai()
    # ID not digits
    elif not id.isdigit():
        print(f'NHVIEW Invalid ID')
        await ctx.send('Invalid ID\nIDs are usually 6 digit numbers, although there are some 5 digin and even shorter or longer IDs\nIf you don\'t have an ID just don\'t write one and we will send you a random doujin :3')
    # Doujin exists?
    elif Hentai.exists(id):
            d = Hentai(id)
            print(f'NHVIEW {id} found')
    else:
        print(f'NHVIEW {id} not found ;-;')
        await ctx.send(f'No Doujin with id: {id} was found\nIf you don\'t have an ID just don\'t write one and we will send you a random doujin :3')

    info={
        'title':d.title(Format.Pretty),
        'url':d.url,
        'color':0xE12754,
        'thumbnail':'https://i.imgur.com/uLAimaY.png',
        'cover':d.cover,
        'footerText':f'ID: {d.id} | {d.num_pages} Pages',
        'extra_fields':[
            {'name':'Artist','value':f"{', '.join(artist.name for artist in d.artist)}"} if d.artist else None,
            {'name':'Language','value':f"{', '.join(lang.name for lang in d.language)}"} if d.language else None,
            {'name':'Group','value':f"{', '.join(group.name for group in d.group)}"} if d.group else None,
            {'name':'Parody','value':f"{', '.join(parody.name for parody in d.parody)}"} if d.parody else None,
            {'name':'Category','value':f"{', '.join(cat.name for cat in d.category)}"} if d.category else None,
            {'name':'Characters','value':f"{', '.join(char.name for char in d.character)}"} if d.character else None,
            {'name':'Tags','value':f"{', '.join(tag.name for tag in d.tag)}",'inline':False} if d.tag else None,

            {'name':'Read','value':':book: React To Read'},
            {'name':'Download','value':f'[:inbox_tray: Torrent](https://nhentai.net/login/?next=%2Fg%2F{d.id}%2Fdownload)'},
            {'name':'Favorite','value':f'[:star: {d.num_favorites}](https://nhentai.net/login/?next=%2Fg%2F{d.id}%2F)'}
        ],
        'showreadbtn': True,
        'read':self.nhr,
        'readargs': {'ctx':ctx, 'id':d.id}
    }

    return await viewmenu.ViewMenu().start(ctx, **info)