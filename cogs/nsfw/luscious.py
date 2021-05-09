import discord
from discord.ext import commands, menus
import asyncio
import json

from luscious import Luscious

import menus.read as readmenu

with open("credentials.json") as f:
    credentials = json.load(f)

async def lc_init(menu):
    l = Luscious(credentials["luscious"]["name"],credentials["luscious"]["password"])
    id = int(menu.extraProcVars['id']) if menu.extraProcVars['id'].isnumeric() else menu.extraProcVars['id']
    c = l.getAlbum(id)
    return {
        'title':c.sanitizedName,
        'url':c.url,
        'footerFormat':'{other}{page}/{total_pages}',
        'footerExtra':f'ID: {c.id} | ',
        'totalPages':c.pictureCount+c.animatedCount,
        'imgURLs':c.contentUrls if c.isManga else c.contentUrls[::-1],
        'extra_fields':[
            {'name':'Tags','value':f"{', '.join(tag.name for tag in c.tags)}",'inline':False} if c.tags else None,
            {'name':'Artists','value':f"{', '.join(artist for artist in c.artists)}",'inline':False} if c.artists else None,
            {'name':'Characters','value':f"{', '.join(character for character in c.characters)}",'inline':False} if c.characters else None,
            {'name':'Audiences','value':f"{', '.join(audience['title'] for audience in c.audiences)}",'inline':False} if c.audiences else None,
            {'name':'Type','value':f"{c.contentType}"+(", Manga" if c.isManga else '')+(", Ongoing" if c.ongoing else ''),'inline':False},
            {'name':'Download','value':f"[:inbox_tray:]({c.downloadUrl})"}
        ]
    }

@commands.command()
async def lctest(self, ctx, *, id, page=1):
    info={
        'color':0xE12754,
        'thumbnail':'https://www.luscious.net/assets/logo-192.png',
        'page':page,
        'showbtns':[True,False,True]*2,
        'init':lc_init,
        'extraProcVars':{'id':id}
    }

    await readmenu.ReadMenu().start(ctx, **info)
