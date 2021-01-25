import discord
from discord.ext import commands
import asyncio

import requests
from bs4 import BeautifulSoup

import menus.read as readmenu

class WebcomicCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def twokinds_init(self, url, page):
        article = BeautifulSoup(requests.get(url).text, 'html.parser').find('article')
        total_pages = int(article.find(class_='navprev')['href'].replace('/','').replace('comic',''))+1
        article = BeautifulSoup(requests.get(url.replace('comic','archive')).text, 'html.parser').find('article')
        chapters= article.find_all(class_='chapter')
    
        chfpg = {}
        for i, ch in enumerate(chapters):
            chfpg[i]=int(ch.find(class_='chapter-links').find(class_='jsdep')['href'].replace('/','').replace('comic',''))

        return {'totalPages':total_pages, 'chfpg':chfpg}

    async def twokinds_proc(self, url, page):
    	twokinds_url = f'{url}{page}' if page!=0 else url
    	article = BeautifulSoup(requests.get(twokinds_url).text, 'html.parser').find('article')
    	page_url = article.find('img')['src']
    	page_title = article.find('h1').text

    	return {'url':page_url, 'title':page_title, 'extra_fields':None,}

    @commands.command()
    async def twokinds(self, ctx, *, page=0):
    	return await readmenu.ReadMenu().start(ctx,
    			url='https://twokinds.keenspot.com/comic/',
    			color=0x72ceef,
    			thumbnail='https://i.imgur.com/YVMsQJ3.png',
    			page=page,
    			footerFormat='{other}{page}/{total_pages}',
    			imgURLbase='https://twokinds.keenspot.com/comic/',
                showbtns=[True,True,True,True,True,True],
                init=self.twokinds_init,
    			proc=self.twokinds_proc
    		)

def setup(client):
    client.add_cog(WebcomicCommands(client))