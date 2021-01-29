import discord
from discord.ext import commands, menus
import asyncio

from luscious_dl import album as lalbum

import menus.read as readmenu
import menus.view as viewmenu

@commands.command()
async def lctest(self, ctx, *, id, page=1):
    a = lalbum.Album(id)
    a.fetch_pictures()
    a.fetch_info()

    info={
        'title':a.title,
        'url':f'https://www.luscious.net/albums/{a.id_}/read/?index=',
        'color':0xE12754,
        'thumbnail':'https://www.luscious.net/assets/logo-192.png',
        'page':page,
        'footerFormat':'{other}{page}/{total_pages} Pages',
        'footerExtra':f'ID: {a.id_} | ',
        'totalPages':a.number_of_pictures,
        'imgURLs':a.pictures,
        'showbtns':[True,False,True]*2
    }

    await readmenu.ReadMenu().start(ctx, **info)