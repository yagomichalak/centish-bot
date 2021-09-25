import discord
from discord.ext import commands
from discord.app.commands import Option, user_command, message_command, slash_command

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
            description=f"💓 **{author.mention} kissed {user.mention}!** 💓",
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

    @slash_command(name="seduce", guild_ids=guild_ids)
    async def _seduce(self, ctx, user: Option(discord.Member, name="user", description="The member to seduce.", required=True)) -> None:
        """ Seduces someone.
        :param user: The member to seduce. """

        author = ctx.author
        if user == author:
            return await ctx.respond(f"**You cannot seduce yourself, lol!**", ephemeral=True)

        if user.bot:
            return await ctx.respond("**You cannot seduce a bot!**", ephemeral=True)

        embed = discord.Embed(
            title="__Seduce__",
            description=f"😏 **{author.mention} seduced {user.mention}!** 😏",
            color=discord.Color.dark_gold()
        )

        seduces: List[str] = [
            'https://c.tenor.com/zM1LLF0voFIAAAAS/butt-touch.gif',
            'https://c.tenor.com/4M8bBOPMpJcAAAAS/unzip-pants.gif',
            'https://c.tenor.com/OgmIkGPBUj4AAAAS/daffy-duck-sexy.gif',
            'https://c.tenor.com/HH9Mte12iuoAAAAS/girlfriends-love.gif',
            'https://c.tenor.com/5K9wKk80s50AAAAS/good-girl-seductive.gif',
            'https://c.tenor.com/2e8Hxp4OczYAAAAS/sexy-seductive.gif',
            'https://c.tenor.com/4kG1mXhlIiQAAAAC/crawl-seductive.gif',
            'https://c.tenor.com/loaJcK1FPgIAAAAS/naked-naughty.gif',
            'https://c.tenor.com/7e9l_2L2RxsAAAAS/natalie-portman-stripping.gif',
            'https://c.tenor.com/n7iFjPuJkYEAAAAS/flaunt-leg.gif',
            'https://c.tenor.com/zEm4_uLqQy8AAAAS/elena-stefan-kiss.gif',
            'https://c.tenor.com/W_dThAW2A4kAAAAS/seductive-seduce.gif',
            'https://c.tenor.com/EkymFviqIT0AAAAC/seductive-making-out.gif',
            'https://c.tenor.com/Fkvp0o1zWMEAAAAC/seductive-himym.gif',
            'https://c.tenor.com/-g0xtwX3t78AAAAC/booty-sexy.gif',
            'https://c.tenor.com/JkElZ-JKqnMAAAAC/flirt-seduce.gif',
            'https://c.tenor.com/NrdehE76Pk4AAAAd/lets-have-sex-seducing.gif',
            'https://c.tenor.com/ksvAUP19DqoAAAAC/seductive-wrap-around.gif',
            'https://c.tenor.com/hYV9SOsmXwYAAAAC/seduce-sexy.gif',
            'https://c.tenor.com/Qag8ifMBgXcAAAAC/garfield-dancing.gif',
            'https://c.tenor.com/gJjz-12AUhAAAAAC/seduce-seduce-you.gif',
            'https://c.tenor.com/WpLww06Z-5UAAAAC/bedroom-eyes.gif',
            'https://c.tenor.com/kTnwtDrGa3UAAAAC/come-here-seductive.gif',
            'https://c.tenor.com/O4dQFZIXhEsAAAAC/flirting.gif',
            'https://c.tenor.com/DdrlDmZdz4QAAAAC/sex-take-your-shirt-off.gif',
            'https://c.tenor.com/l7k9gBs8ZwUAAAAC/ohreally-sexy.gif',
            'https://c.tenor.com/9tVeJFB8HIgAAAAC/seductive-sexy.gif',
            'https://c.tenor.com/hk09Npo8YpEAAAAC/marshall-jason-segel.gif',
            'https://c.tenor.com/9gGVdXCua4IAAAAC/zoe-hart-flirt.gif',
            'https://c.tenor.com/ct1MXPbyJ1MAAAAd/such-beaty-smell.gif',
            'https://c.tenor.com/Z1wp97tfbUsAAAAC/bath-legs.gif',
            'https://c.tenor.com/ieVgdmsFlhgAAAAC/seduce-hot.gif',
            'https://c.tenor.com/QtHsQnlce9sAAAAC/kiss-wink.gif',
            'https://c.tenor.com/7KEZ3UywoyIAAAAC/eyebrows-seductive.gif',
            'https://c.tenor.com/xhHErbzZz6sAAAAC/sexy-wink.gif',
            'https://c.tenor.com/La3-ZgjSRxgAAAAC/wiggle-shimmy.gif'
        ]

        embed.set_author(name=author, icon_url=author.display_avatar)
        embed.set_image(url=choice(seduces))
        embed.set_footer(text=user, icon_url=user.display_avatar)

        await ctx.respond(embed=embed)


def setup(client: commands.Bot) -> None:
    """ Cog's setup function. """

    client.add_cog(RolePlay(client))