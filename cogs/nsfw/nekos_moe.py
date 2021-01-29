import json

import discord
from discord.ext import commands, menus
import asyncio

from PyNekos.nekosapi import Neko

import menus.view as viewmenu

# Nekos.moe
@commands.command()
async def nm(self, ctx):
    print(f'Nekos.moe...')

    nyan = Neko()
    kw = {
        'nsfw': True,
        'count': 1
    }

    res=nyan.random_image(**kw)['images'][0]

    info={
        'title':'Nekos.moe',
        'url':res['url'],
        'color':0xE4DADA,
        'thumbnail':'https://github.com/Nekos-moe/website/raw/master/static/images/logo.jpg',
        'cover':res['url'],
        'footerText':json.dumps(res['uploader']).replace('"','').replace('{','').replace('}','')
    }

    return await viewmenu.ViewMenu().start(ctx, **info)