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
        await interaction.response.defer()
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
        embed.set_footer(text=f"{len(self.words)} result(s).")
        return embed


    async def update_page(self, message: discord.Message) -> None:
        """ Updates the page and its original embedded message. """

        embed = await self.get_page()
        await message.edit(embed=embed)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return self.member.id == interaction.user.id


class ConjugationView(discord.ui.View):
    """ View for conjugation pagination."""

    def __init__(self, member: Union[discord.Member, discord.User], data: Dict[str, Any], timeout: Optional[float] = None):
        super().__init__(timeout=timeout)
        self.member = member
        self.verb: Dict[str, Any] = data.get('verb')
        self.tenses: Dict[str, Union[str, None]] = data.get('tenses')
        self.index: int = 0
        self.current_page: int = 0
        self.per_page = 3
        self.conjugations: List[Dict[str, str]] = []

    async def start(self) -> discord.Embed:
        """ Starts the conjugation view. """

        # conjugations: List[Dict[str, str]] = {}

        text: str = ''
        for tense, info in self.tenses.items():

            verb_root: str = self.verb['word'].lower()[:-3]


            if suffix := info['suffix']:
                conjugation: str = verb_root + suffix
            else:
                conjugation: str = verb_root

            pronouns: List[str] = ['Qk', 'Dk', 'Hk', 'Sk', 'Tk', 'Wk', 'Mk']
            rows: str = '\n'.join([f'{pn} {conjugation}' if tense != 'Imperative' else conjugation.capitalize() for pn in pronouns])
            text: str = f"```apache\n{rows}```"

            self.conjugations.append({"tense": tense, "text": text})

        return await self.get_page()


    @discord.ui.button(style=discord.ButtonStyle.success, label="Left", custom_id="go_left_id")
    async def left_page(self, button: discord.ui.button, interaction: discord.Interaction) -> None:
        
        await interaction.response.defer()

        if self.index - self.per_page >= 0:
            self.index -= self.per_page
            self.current_page -= 1
            await self.update_page(interaction.message)

    @discord.ui.button(style=discord.ButtonStyle.success, label="Right", custom_id="go_right_id")
    async def right_page(self, button: discord.ui.button, interaction: discord.Interaction) -> None:

        await interaction.response.defer()

        if len(self.conjugations) >= self.index + self.per_page:
            self.index += self.per_page
            self.current_page += 1
            await self.update_page(interaction.message)

    @discord.ui.button(style=discord.ButtonStyle.danger, label="Stop", custom_id="stop_id")
    async def stop_page(self, button: discord.ui.button, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        self.stop()

    async def get_page(self) -> discord.Embed:

        current_date = await utils.get_time_now('Europe/Rome')

        # Creates basic embed
        embed = discord.Embed(
            title=f"__Centish Conjugation__: ({self.current_page+1}/{round(len(self.conjugations)/self.per_page)})",
            description=f"**Verb:** {self.verb['word']} | **Translation:** {self.verb['translation']}",
            color=self.member.color,
            timestamp=current_date
        )

        conjugations = self.conjugations[self.index:self.index+self.per_page]
        for conj in conjugations:
            embed.add_field(name=f"__{conj['tense']}__", value=conj['text'], inline=True)

        return embed


    async def update_page(self, message: discord.Message) -> None:
        """ Updates the page and its original embedded message. """

        embed = await self.get_page()
        await message.edit(embed=embed)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return self.member.id == interaction.user.id