import discord
from discord.ext import commands
from typing import Optional


class Moderation(commands.Cog):
    """ Category for moderation tools and commands. """

    def __init__(self, client) -> None:
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """ Tells when the cog is ready to go. """

        print('Moderation cog is online!')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount=0, member: Optional[discord.Member] = None):
        """ (MOD) Purges messages.
        :param amount: The amount of messages to purge.
        :param member: The member from whom to purge the messages. (Optional) """

        perms = ctx.channel.permissions_for(ctx.author)
        if not perms.administrator:
            if amount >= 30:
                return await ctx.send(f"**You cannot delete more than `30` messages at a time, {ctx.author.mention}!**")

        await ctx.message.delete()
        # Global deleted
        deleted = 0
        if member:
            channel = ctx.channel
            msgs = list(filter(
                lambda m: m.author.id == member.id,
                await channel.history(limit=200).flatten()
            ))
            for _ in range(amount):
                await msgs.pop(0).delete()
                deleted += 1

            await ctx.send(f"**`{deleted}` messages deleted for `{member}`**",
                delete_after=5)

        else:
            await ctx.channel.purge(limit=amount)


def setup(client) -> None:
    """ Cog's setup funciton. """

    client.add_cog(Moderation(client))