import discord
from discord.app.commands import slash_command
from discord.ext import commands
from extra import utils
from typing import Union, List
from extra.language.centish import Centish

from PIL import ImageDraw, ImageFont, Image
import aiohttp
import os

guild_ids: List[int] = [int(os.getenv('SERVER_ID'))]
dnk_id = int(os.getenv('DNK_ID'))
cent_id = int(os.getenv('CENT_ID'))

class Social(commands.Cog):
    """ Category for social related commands. """

    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        self.session = aiohttp.ClientSession()


    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """ Tells when the cog is ready to go. """

        print("Social cog is online!")

    @commands.command(aliases=['si', 'server'])
    async def serverinfo(self, ctx) -> None:
        """ Shows information about the server. """

        guild = ctx.guild

        em = discord.Embed(description=guild.description, color=ctx.author.color)
        online = len({m.id for m in guild.members if m.status is not discord.Status.offline})
        em.add_field(name="Server ID", value=guild.id, inline=True)
        em.add_field(name="Server Owner", value=guild.owner.mention, inline=False)
        em.add_field(name="Conlang Creators", value=f"<@{dnk_id}> & <@{cent_id}> 💞", inline=False)

        em.add_field(name="Members", value=f"🟢 {online} members ⚫ {len(guild.members)} members", inline=True)
        em.add_field(name="Channels",
            value=f"⌨️ {len(guild.text_channels)} | 🔈 {len(guild.voice_channels)} | 📻 {len(guild.stage_channels)} | 📁 {len(guild.categories)} | **=** {len(guild.channels)}",
            inline=False)
        em.add_field(name="Roles", value=len(guild.roles), inline=True)
        em.add_field(name="Emojis", value=len(guild.emojis), inline=True)
        em.add_field(name="🌐 Region", value=str(guild.region).title() if guild.region else None, inline=True)
        em.add_field(name="🌟 Boosts", value=f"{guild.premium_subscription_count} (Level {guild.premium_tier})", inline=True)
        features = ', '.join(list(map(lambda f: f.replace('_', ' ').capitalize(), guild.features)))
        em.add_field(name="Server Features", value=features if features else None, inline=False)

        em.set_thumbnail(url=guild.icon.url)
        if guild.banner:
            em.set_image(url=guild.banner.url)
        em.set_author(name=guild.name, icon_url=guild.icon.url)
        created_at = await utils.sort_time(guild.created_at)
        em.set_footer(text=f"Created: {guild.created_at.strftime('%d/%m/%y')} ({created_at})")
        await ctx.send(embed=em)

    @commands.command(aliases=['user', 'whois', 'who_is'])
    async def userinfo(self, ctx, member: Union[discord.Member, discord.User] = None):
        """ Shows all the information about a member.
        :param member: The member to show the info.
        :return: An embedded message with the user's information. """

        member = ctx.author if not member else member

        embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)

        embed.set_author(name=f"User Info: {member}")
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)

        embed.add_field(name="ID:", value=member.id, inline=False)

        if hasattr(member, 'guild'):
            embed.add_field(name="Guild name:", value=member.display_name, inline=False)
            sorted_time_create = f"<t:{int(member.created_at.timestamp())}:R>"
            sorted_time_join = f"<t:{int(member.joined_at.timestamp())}:R>"

            embed.add_field(name="Created at:", value=f"{member.created_at.strftime('%d/%m/%y')} ({sorted_time_create}) **GMT**",
                            inline=False)
            embed.add_field(name="Joined at:", value=f"{member.joined_at.strftime('%d/%m/%y')} ({sorted_time_join}) **GMT**", inline=False)

            embed.add_field(name="Top role:", value=member.top_role.mention, inline=False)

        embed.add_field(name="Bot?", value=member.bot)
        await ctx.send(embed=embed)


    @commands.command(name="kingdom_image", aliases=["kingdom", "castle"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _kingdom_image_command(self, ctx) -> None:
        """ Makes the Centish kingdom image. """

        await self._kingdom_image_callback(ctx)

    @slash_command(name="kingdom_image", guild_ids=guild_ids)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _kingdom_image_slash(self, ctx) -> None:
        """ Makes the Centish kingdom image. """
        
        await self._kingdom_image_callback(ctx)

    async def _kingdom_image_callback(self, ctx) -> None:
        """ Makes the Centish kingdom image. """

        member = ctx.author

        answer: discord.PartialMessageable = None
        
        if isinstance(ctx, commands.Context):
            answer = ctx.send
        else:
            await ctx.defer()
            answer = ctx.respond

        # Get conlang creators
        cent: discord.User = await self.client.fetch_user(int(os.getenv('CENT_ID')))
        dnk: discord.User = await self.client.fetch_user(int(os.getenv('DNK_ID')))

        # Images
        img_root: str = 'media/images/'
        background: Image.Image = Image.open(f"{img_root}dark_bg.jpg").resize((400, 400)).convert('RGBA')
        kingdom: Image.Image = Image.open(f"{img_root}kingdom_castle.png").resize((400, 400)).convert('RGBA')
        cent_pfp: Image.Image = await utils.get_user_pfp(cent)
        dnk_pfp: Image.Image = await utils.get_user_pfp(dnk)
        moon: Image.Image = Image.open(f"{img_root}crescent_moon.png").resize((50, 50))
        symbol: Image.Image = Image.open(f"{img_root}white_cent_symbol.png").resize((50, 50))
        hearts: Image.Image = Image.open(f"{img_root}hearts.png").resize((35, 35))

        # Paste images
        background.paste(kingdom, (0, 0), kingdom)
        background.paste(cent_pfp, (90, 70), cent_pfp)
        background.paste(dnk_pfp, (250, 70), dnk_pfp)
        background.paste(moon, (33, 230), moon)
        background.paste(moon, (319, 230), moon)
        background.paste(symbol, (176, 90), symbol)
        background.paste(hearts, (185, 165), hearts)

        # Gets font and writes text
        font_path: str = "media/fonts/built titling sb.ttf"
        micro = ImageFont.truetype(font_path, 25)
        tiny = ImageFont.truetype(font_path, 30)
        small = ImageFont.truetype(font_path, 45)

        # General info
        draw = ImageDraw.Draw(background)
        draw.text((98, 142), "cent", (255, 255, 255), font=tiny)
        draw.text((262, 142), "DNK", (255, 255, 255), font=tiny)
        draw.text((124, 245), "Cajdklaje", (255, 255, 255), font=small)

        # Word counter
        draw.text((35, 285), "Words", (255, 255, 255), font=micro)
        words = await Centish.get_words()
        draw.text((35, 325), str(len(words['words'])), (255, 255, 255), font=micro)

        # Creation date
        draw.text((295, 285), "Creation", (255, 255, 255), font=micro)
        draw.text((295, 325), "08/17/21", (255, 255, 255), font=micro)

        # Saves the final image
        file_path: str = f'media/images/temp/result_{member.id}.png'
        background.save(file_path, 'png', quality=90)


        current_time = await utils.get_time_now('Europe/Rome')
        # Makes the embed
        embed = discord.Embed(
            title="__Cajdklaje Rezom__",
            description="Tuzim informazza sout cajdklaje rezom.",
            # color=int("000001", 16),
            color=int("d070da", 16),
            timestamp=current_time
        )
        embed.set_thumbnail(url="https://images.emojiterra.com/twitter/v13.0/512px/262a.png")
        embed.set_image(url="attachment://kingdom.png")
        embed.set_author(name=self.client.user, icon_url=self.client.user.display_avatar)
        embed.set_footer(text=f"Requested by {member}", icon_url=member.display_avatar)

        try:
            await answer(embed=embed, file=discord.File(file_path, filename="kingdom.png"))
        except:
            pass
        finally:
            os.remove(file_path)

def setup(client) -> None:
    """ Cog's setup function. """
    
    client.add_cog(Social(client))