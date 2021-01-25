import discord
from discord.ext import commands
import asyncio

import requests
from bs4 import BeautifulSoup

import menus.read as readmenu

class WebcomicCommands(commands.Cog):
    def __init__(self, client):
        self.client = client


    async def twokinds_proc(self, url, page):
    	twokinds_url = f'{url}comic/{page}' if page!=0 else url
    	article = BeautifulSoup(requests.get(twokinds_url).text, 'html.parser').find('article')
    	page_url = article.find('img')['src']
    	page_title = article.find('h1').text

    	twokinds_url = url
    	article = BeautifulSoup(requests.get(twokinds_url).text, 'html.parser').find('article')

    	total_pages = int(article.find(class_='navprev')['href'].replace('/','').replace('comic',''))+1
    	print(total_pages)
    	return {'url':page_url, 'title':page_title, 'totalPages':total_pages, 'extra_fields':None,}

    @commands.command()
    async def twokinds(self, ctx, *, page=0):
    	return await readmenu.ReadMenu().start(ctx,
    			url='https://twokinds.keenspot.com/',
    			color=0x72ceef,
    			thumbnail='https://i.imgur.com/YVMsQJ3.png',
    			page=page,
    			footerFormat='{other}{page}/{total_pages}',
    			imgURLbase='https://twokinds.keenspot.com/',
    			imgURLproc=self.twokinds_proc
    		)

def setup(client):
    client.add_cog(WebcomicCommands(client))