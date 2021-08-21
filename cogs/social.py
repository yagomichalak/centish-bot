import discord
from discord.ext import commands
from extra import utils
import os

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


def setup(client) -> None:
    """ Cog's setup function. """
    
    client.add_cog(Social(client))