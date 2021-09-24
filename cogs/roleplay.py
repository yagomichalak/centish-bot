import discord
from discord.ext import commands
from discord.app.commands import user_command, message_command, slash_command

from typing import List
import os
from random import choice

guild_ids: List[int] = [int(os.getenv('SERVER_ID'))]

class RolePlay(commands.Cog):
    """ Category for role playing commands. """


    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """ Tells when the cog is ready to go. """

        print('RolePlay cog is online!')

    @user_command(name="Pat", guild_ids=guild_ids)
    async def _pat(self, ctx, user: discord.Member) -> None:
        """ Pats someone. """

        await ctx.respond(f"**{ctx.author.mention} patted {user.mention}!**")

    @user_command(name="Kiss", guild_ids=guild_ids)
    async def _kiss(self, ctx, user: discord.Member) -> None:
        """ Kisses someone. """

        author = ctx.author
        if user == author:
            return await ctx.respond(f"**You cannot kiss yourself, lol!**", ephemeral=True)

        if user.bot:
            return await ctx.respond("**You cannot kiss a bot!**", ephemeral=True)

        embed = discord.Embed(
            title="__Kiss__",
            description=f"💓 **{ctx.author.mention} kissed {user.mention}!** 💓",
            color=discord.Color.brand_red()
        )

        kisses: List[str] = [
            'https://c.tenor.com/sx0mJIjy61gAAAAC/milk-and-mocha-bear-couple.gif',
            'https://c.tenor.com/hK8IUmweJWAAAAAC/kiss-me-%D0%BB%D1%8E%D0%B1%D0%BB%D1%8E.gif',
            'https://c.tenor.com/Aaxuq2evHe8AAAAC/kiss-cute.gif',
            'https://c.tenor.com/A0ixOj7Y1WUAAAAC/kiss-anime.gif',
            'https://c.tenor.com/ErAPuiWY46QAAAAC/kiss-anime.gif',
            'https://c.tenor.com/4GdkzkTQdI8AAAAC/kissing-love.gif',
            'https://c.tenor.com/lsOkG57_ibIAAAAd/kiss-lip-kiss.gif',
            'https://c.tenor.com/uF0-jdZRkLYAAAAC/kissing-kiss.gif',
            'https://c.tenor.com/3kvvlXjRse0AAAAC/kiss-lip-kiss.gif',
            'https://c.tenor.com/RZEZVjS3MeMAAAAC/forcibly-kissing-deep-kiss.gif',
            'https://c.tenor.com/teTesMTK_c4AAAAC/shiksha-wedding.gif',
            'https://c.tenor.com/RrUKz9kC3bUAAAAi/dovey-bunnies-kisses.gif',
            'https://c.tenor.com/FDcq03ZLNX0AAAAi/love-couple.gif',
            'https://c.tenor.com/LbOTuZXj9y4AAAAC/cat-love.gif',
            'https://c.tenor.com/OhTr6EO7u14AAAAC/love-you-kiss.gif',
            'https://c.tenor.com/xTSmPl72UjYAAAAC/kiss-blushing.gif',
            'https://c.tenor.com/Gr8BaRWOudkAAAAC/brown-and-cony-kiss.gif',
            'https://c.tenor.com/uhB9b3AzxrQAAAAC/brown.gif',
            'https://c.tenor.com/cK2c6eQ7Is8AAAAC/cony-and-brown-hug.gif',
            'https://c.tenor.com/sXNJMF5vI8oAAAAC/love-peachcat.gif',
            'https://c.tenor.com/MXd8Xby7jnMAAAAC/davydoff-love.gif',
            'https://c.tenor.com/yWGhrAd0cioAAAAC/kissing-couple.gif'

        ]

        embed.set_author(name=author, icon_url=author.display_avatar)
        embed.set_image(url=choice(kisses))
        embed.set_footer(text=user, icon_url=user.display_avatar)

        await ctx.respond(embed=embed)


def setup(client: commands.Bot) -> None:
    """ Cog's setup function. """

    client.add_cog(RolePlay(client))