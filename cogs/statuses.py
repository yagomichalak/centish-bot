import discord
from discord.ext import commands, tasks
import os
from typing import Dict, Union, Any
from extra import utils
from extra.language.centish import Centish


class Statuses(commands.Cog):
    """ Category for server status related commands and features. """

    def __init__(self, client) -> None:
        self.client = client
        self.status_channels: Dict[str, int] = {
            "Clock": int(os.getenv('CLOCK_CHANNEL_ID')),
            "Word": int(os.getenv('WORD_COUNT_CHANNEL_ID')),
            "Member": int(os.getenv('MEMBER_COUNT_CHANNEL_ID')),
            "Boost": int(os.getenv('BOOST_COUNT_CHANNEL_ID'))
        }

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """ Tells when the cog is ready to run. """

        self.update_status_channels.start()
        print('Statuses cog is ready')


    @tasks.loop(minutes=6)
    async def update_status_channels(self) -> None:
        """ Updates all server status channels. """

        guild: discord.Guild = self.client.get_guild(int(os.getenv('SERVER_ID')))

        for status_channel, channel_id in self.status_channels.items():
            if channel := self.client.get_channel(channel_id):

                updated_message: str = ''

                if status_channel == 'Clock': # Updates the clock channel.
                    updated_message = f"🕐 GMT+2 - {(await utils.get_time_now('Europe/Rome')).strftime('%H:%M')}"

                elif status_channel == 'Word': # Updates the word count channel.
                    updated_message = f"☪️ {len((await Centish.get_words())['words'])} words"

                elif status_channel == 'Member': # Updates the member count channel.
                    updated_message = f"👥 {len(guild.members)} members" 

                elif status_channel == 'Boost': # Updates the boost count channel.
                    updated_message = f"✨ {guild.premium_subscription_count} boosts"

                try:
                    await channel.edit(name=updated_message)
                except:
                    continue


def setup(client) -> None:
    """ Cog's setup function. """

    client.add_cog(Statuses(client))