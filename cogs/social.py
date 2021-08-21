import discord
from discord.ext import commands
from extra import utils
import os
from typing import Union

dnk_id = int(os.getenv('DNK_ID'))
cent_id = int(os.getenv('CENT_ID'))

class Social(commands.Cog):
    """ Category for social related commands. """

    def __init__(self, client: commands.Bot) -> None:
        self.client = client


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

def setup(client) -> None:
    """ Cog's setup function. """
    
    client.add_cog(Social(client))