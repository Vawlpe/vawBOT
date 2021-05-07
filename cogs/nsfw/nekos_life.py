import discord
from discord.ext import commands, menus
import asyncio

import nekos

import menus.view as viewmenu

# NekosLife
@commands.command()
async def nl(self, ctx, *, tag):
    print(f'Nekos.life {tag}...')

    info={
        'title':f'{tag}#{"".join(filter(str.isdigit, tag))}',
        'url':tag,
        'color':0xE12754,
        'thumbnail':'https://nekos.life/static/icons/favicon-194x194.png',
        'cover':nekos.img(tag),
        'footerText':f'nekos.life: {tag}'
    }

    return await viewmenu.ViewMenu().start(ctx, **info)
