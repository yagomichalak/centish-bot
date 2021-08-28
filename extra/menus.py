import discord
from discord import utils
from discord.ext import commands
from typing import Union, Any, List, Dict, Optional
from extra import utils


class WordPaginationView(discord.ui.View):
    """ View for word pagination."""

    def __init__(self, member: Union[discord.Member, discord.User], data: Dict[str, Any], timeout: Optional[float] = None):
        super().__init__(timeout=timeout)
        self.member = member
        self.words: List[Dict[str, str]] = data.get('words')
        self.word_type = data.get('word_type')
        self.index: int = 0
        self.per_page = 15


    @discord.ui.button(style=discord.ButtonStyle.success, label="Left", custom_id="go_left_id")
    async def left_page(self, button: discord.ui.button, interaction: discord.Interaction) -> None:
        
        await interaction.response.defer()

        if self.index - self.per_page >= 0:
            self.index -= self.per_page
            await self.update_page(interaction.message)

    @discord.ui.button(style=discord.ButtonStyle.success, label="Right", custom_id="go_right_id")
    async def right_page(self, button: discord.ui.button, interaction: discord.Interaction) -> None:

        await interaction.response.defer()

        if len(self.words) >= self.index + self.per_page:
            self.index += self.per_page
            await self.update_page(interaction.message)

    @discord.ui.button(style=discord.ButtonStyle.danger, label="Stop", custom_id="stop_id")
    async def stop_page(self, button: discord.ui.button, interaction: discord.Interaction) -> None:
        self.stop()

    async def get_page(self) -> discord.Embed:

        current_date = await utils.get_time_now()

        # Creates basic embed
        embed = discord.Embed(
            title=f"__Showing Words__: ({self.word_type.title()})",
            color=self.member.color,
            timestamp=current_date
        )

        words = self.words[self.index:self.index+self.per_page]
        
        # Makes header
        temp_text1 = f"{'[Word]':^12} | {'[Translation]':<13} | {'[Types]':^15}"
        embed.add_field(
            name=f"{'='*52}",
            value=f"```ini\n{temp_text1}```",
            inline=False
        )

        # Formats words
        formatted_words = [
            f"""{w['word']:<12} | {w['translation']:<13} | {', '.join(
                [wt[:3] for wt in w['types']]
                ):>15}""" for w in words
        ]
        formatted_words = '\n'.join(formatted_words)

        # Creates field for formatted words
        embed.add_field(
            name=f"{'='*52}",
            value=f"```apache\n{formatted_words}```",
            inline=False
        )
        return embed


    async def update_page(self, message: discord.Message) -> None:
        """ Updates the page and its original embedded message. """

        embed = await self.get_page()
        await message.edit(embed=embed)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return self.member.id == interaction.user.id