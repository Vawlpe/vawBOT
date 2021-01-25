import discord
from discord.ext import menus
import asyncio

class ReadMenu(menus.Menu):
    async def start(self, ctx, title=None, url=None, color=None, thumbnail=None, page=None, footerFormat=None, extra_fields=None, totalPages=None, imgURLs=None, imgURLbase=None, imgURLproc=None):
        self.title=title
        self.url=url
        self.color=color
        self.thumbnail=thumbnail
        self.page=page
        self.footerFormat=footerFormat
        self.extra_fields=extra_fields
        self.totalPages=totalPages
        self.imgURLs=imgURLs
        self.imgURLbase=imgURLbase
        self.imgURLproc=imgURLproc
        await super().start(ctx)

    async def domsg(self, ctx=None):
        # Create Embed...
        embed=discord.Embed(
            color=self.color,
            title=self.title,
            url=f'{self.url}{self.page}'
        )
        embed.set_thumbnail(url=self.thumbnail)

        # Get the main image
        if self.imgURLs is not None:
            # Use URL list[page]
            embed.set_image(url=self.imgURLs[self.page-1])
            self.totalPages=len(imgURLs)
        elif self.imgURLproc is None:
            # Use URL base/page
            embed.set_image(url=f'{self.imgURLbase}comic/{self.page}')
        else:
            # Preprocess URL base/page
            processed=await self.imgURLproc(self.imgURLbase, self.page)
            embed.set_image(url=processed['url'])
            if processed['title'] is not None:
                embed.title=processed['title']

            if processed['extra_fields'] is not None:
                self.extra_fields=processed['extra_fields']

            if processed['totalPages'] is not None:
                self.totalPages=processed['totalPages']

        if self.page==0:
                    self.page=self.totalPages

        if self.extra_fields is not None:
            for f in self.extra_fields:
                embed.add_field(**f)

        embed.set_footer(text=self.footerFormat.format(other='',page=self.page, total_pages=self.totalPages))

        # Send or Edit
        if self.message is None:
            return await ctx.send(embed=embed)
        else:
            await self.message.edit(embed=embed)

    async def send_initial_message(self, ctx, channel):
        return await self.domsg(ctx)

    @menus.button('⏮️')
    async def on_start(self, payload):
        self.page=1
        await self.domsg()

    @menus.button('⬅️')
    async def on_prev(self, payload):
        self.page=max(1, min(self.page-1, self.totalPages))
        await self.domsg()

    @menus.button('➡️')
    async def on_next(self, payload):
        self.page=max(1, min(self.page+1, self.totalPages))
        await self.domsg()

    @menus.button('⏭️')
    async def on_end(self, payload):
        self.page=self.totalPages
        await self.domsg()