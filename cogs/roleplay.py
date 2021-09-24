import discord
from discord.ext import commands
from discord.app.commands import user_command, message_command, slash_command

class RolePlay(commands.Cog):
    """ Category for role playing commands. """


    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """ Tells when the cog is ready to go. """

        print('RolePlay cog is online!')


def setup(client: commands.Bot) -> None:
    """ Cog's setup function. """

    client.add_cog(RolePlay(client))