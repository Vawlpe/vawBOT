import discord
from discord.ext import menus
import asyncio

class ReadMenu(menus.Menu):
    async def start(self, ctx, title=None, url=None, color=None, thumbnail=None, page=None, footerFormat='{page}/{total_pages}', footerExtra='', extra_fields=None, totalPages=None, imgURLs=None, imgURLbase=None, showbtns={True,False,True,True,False,True}, init=None, proc=None):
        self.title=title
        self.url=url
        self.color=color
        self.thumbnail=thumbnail
        self.page=page
        self.footerFormat=footerFormat
        self.footerExtra=footerExtra
        self.extra_fields=extra_fields
        self.totalPages=totalPages
        self.imgURLs=imgURLs
        self.imgURLbase=imgURLbase
        self.showbtns=showbtns
        self.init=init
        self.proc=proc
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
            self.totalPages=len(self.imgURLs)
        elif self.proc is None:
            # Use URL base/page
            embed.set_image(url=f'{self.imgURLbase}{self.page}')
        else:
            # Proc URL base/page
            processed=await self.proc(self.imgURLbase, self.page)
            embed.set_image(url=processed['url'])
            if processed['title'] is not None:
                embed.title=processed['title']

            if processed['extra_fields'] is not None:
                self.extra_fields=processed['extra_fields']

            for i, ch in enumerate(self.chfpg):
                if self.chfpg[i]>self.page:
                    self.currch=i-1
                    break

        if self.page==0:
                    self.page=self.totalPages

        if self.extra_fields is not None:
            for f in self.extra_fields:
                embed.add_field(**f)

        embed.set_footer(text=self.footerFormat.format(other=self.footerExtra ,page=self.page, total_pages=self.totalPages))

        # Send or Edit
        if self.message is None:
            return await ctx.send(embed=embed)
        else:
            await self.message.edit(embed=embed)

    async def send_initial_message(self, ctx, channel):
        if self.init is not None:
            proc = await self.init(self.imgURLbase, self.page)
            if proc['totalPages'] is not None:
                self.totalPages=proc['totalPages']

            if proc['chfpg'] is not None:
                self.chfpg=proc['chfpg']

        return await self.domsg(ctx)

    def show_start(self):
        return not self.showbtns[0]

    def show_prevch(self):
        return not self.showbtns[1]

    def show_prev(self):
        return not self.showbtns[2]

    def show_next(self):
        return not self.showbtns[3]

    def show_nextch(self):
        return not self.showbtns[4]

    def show_end(self):
        return not self.showbtns[5]

    @menus.button('⏮️',skip_if=show_start)
    async def on_start(self, payload):
        self.page=1
        await self.domsg()

    @menus.button('⏪',skip_if=show_prevch)
    async def on_prevch(self, payload):
        self.page=max(1, min(self.chfpg[self.currch-1], self.totalPages))
        await self.domsg()

    @menus.button('⬅️',skip_if=show_prev)
    async def on_prev(self, payload):
        self.page=max(1, min(self.page-1, self.totalPages))
        await self.domsg()

    @menus.button('➡️',skip_if=show_next)
    async def on_next(self, payload):
        self.page=max(1, min(self.page+1, self.totalPages))
        await self.domsg()

    @menus.button('⏩',skip_if=show_nextch)
    async def on_nextch(self, payload):
        self.page=max(1, min(self.chfpg[self.currch+1], self.totalPages))
        await self.domsg()

    @menus.button('⏭️',skip_if=show_end)
    async def on_end(self, payload):
        self.page=self.totalPages
        await self.domsg()