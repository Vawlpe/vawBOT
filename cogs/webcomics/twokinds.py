import discord
from discord.ext import commands
import asyncio

import menus.read as readmenu

import requests
from bs4 import BeautifulSoup

async def twokinds_init(self):
    url = self.imgURLbase
    page = self.page
    article = BeautifulSoup(requests.get(url).text, 'html.parser').find('article')
    total_pages = int(article.find(class_='navprev')['href'].replace('/','').replace('comic',''))+1
    article = BeautifulSoup(requests.get(url.replace('comic','archive')).text, 'html.parser').find('article')
    chapters= article.find_all(class_='chapter')

    chfpg = {}
    for i, ch in enumerate(chapters):
        chfpg[i]=int(ch.find(class_='chapter-links').find('a')['href'].replace('/','').replace('comic',''))

    return {'totalPages':total_pages, 'chfpg':chfpg}

async def twokinds_proc(self):
    url = self.imgURLbase
    page = self.page
    twokinds_url = f'{url}{page}' if page!=0 else url
    article = BeautifulSoup(requests.get(twokinds_url).text, 'html.parser').find('article')
    page_url = article.find('img')['src']
    page_title = article.find('h1').text

    return {'url':page_url, 'title':page_title, 'extra_fields':None,}

@commands.command()
async def twokinds(self, ctx, *, page=0):
    info={
        'url':'https://twokinds.keenspot.com/comic/',
        'color':0x72ceef,
        'thumbnail':'https://i.imgur.com/YVMsQJ3.png',
        'page':page,
        'footerFormat':'{page}/{total_pages}',
        'imgURLbase':'https://twokinds.keenspot.com/comic/',
        'showbtns':[True]*6,
        'init':twokinds_init,
        'proc':twokinds_proc
    }
    return await readmenu.ReadMenu().start(ctx,**info)
