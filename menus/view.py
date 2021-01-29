import discord
from discord.ext import menus
import asyncio


class ViewMenu(menus.Menu):
    async def start(self, ctx, title=None, url=None, color=None, thumbnail=None, cover=None, footerFormat='{other}', footerText='Default footerText', extra_fields=None, showreadbtn=False, init=None, proc=None, read=None, readargs=None):
        self.title=title
        self.url=url
        self.color=color
        self.thumbnail=thumbnail
        self.cover=cover
        self.footerFormat=footerFormat
        self.footerText=footerText
        self.extra_fields=extra_fields
        self.showreadbtn=showreadbtn
        self.init=init
        self.read=read
        self.readargs=readargs
        await super().start(ctx)

    async def send_initial_message(self, ctx, channel):
        if self.init is not None:
            proc=await self.init(self.url)
        
        embed=discord.Embed(color=self.color, 
            title=self.title,
            url=self.url
        )
        embed.set_thumbnail(url=self.thumbnail)
        embed.set_image(url=self.cover)

        if self.extra_fields is not None:
            for f in self.extra_fields:
                if f is not None:
                    embed.add_field(**f)

        embed.set_footer(text=self.footerFormat.format(other=self.footerText))

        return await ctx.send(embed=embed)

    def show_read(self):
        return not self.showreadbtn

    @menus.button('\N{OPEN BOOK}',skip_if=show_read)
    async def on_book_open(self, payload):
        await self.message.delete()
        await self.read(**self.readargs)
        self.stop()