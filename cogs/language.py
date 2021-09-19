import discord
from discord.ext import commands
from extra.language.centish import Centish
from typing import Optional, List
from extra.menus import WordPaginationView
from extra import utils

class Language(commands.Cog, Centish):
    """ Category for commands related to the Centish language. """

    def __init__(self, client) -> None:
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """ Tells when the cog is ready to go. """

        print('Language cog is online!')

    @commands.command(name="word_count", aliases=['wc', "words_count", "count_words"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _word_count_command(self, ctx) -> None:
        """ Tells how many words there are currently in the Centish language. """

        await self._word_count(ctx)

    async def _word_count(self, ctx) -> None:
        """ Tells how many words there are currently in the Centish language. """

        answer: discord.PartialMessageable = ctx.send if isinstance(ctx, commands.Context) else ctx.respond

        words = await self.get_words()
        await answer(
            f"**There are currently `{len(words['words'])}` words in the `Centish` language, {ctx.author.mention}!**")

    
    @commands.command(name="words")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _words_command(self, ctx, word_type: Optional[str] = None) -> None:
        await self._words(ctx, word_type)


    async def _words(self, ctx, word_type: Optional[str] = None) -> None:
        """ Shows Centish words.

        :param word_type: The type of word to show. [Optional][Default=All] """

        author = ctx.author
        answer: discord.PartialMessageable = None

        if isinstance(ctx, commands.Context):
            answer = ctx.send
        else:
            await ctx.defer()
            answer = ctx.followup.send

        accepted_word_types: List[str] = [
            'adjective', 'noun', 'adverb', 'verb', 'exclamation', 
            'question', 'pronoun', 'conjunction', 'preposition'
        ]

        if word_type:
            if word_type.lower() not in accepted_word_types:
                return await answer(f"**Please, inform a valid `word type`, {author.mention}!**\n{', '.join(accepted_word_types)}")

        words = await self.get_words()
        words = words['words']
        if word_type:
            words = await self.filter_words(words, word_type)
        else:
            word_type = 'all'

        data = {
            'word_type': word_type,
            'words': words
        }

        # Paginates word list
        view = WordPaginationView(author, data)
        embed = await view.get_page()

        msg = await answer(embed=embed, view=view)

        await view.wait()
        await utils.disable_buttons(view)
        await msg.edit(view=view)


    async def _conjugate_callback(self, ctx, verb: str) -> None:
        """ Conjugates a verb in Centish.
        :param verb: The verb to conjugate. """

        answer: discord.PartialMessageable = ctx.send if isinstance(ctx, commands.Context) else ctx.followup.send


        words = await Centish.get_words()
        filtered_words = await Centish.filter_words(words['words'], 'verb')
        found = await Centish.find_words(verb, filtered_words, multiple=False)
        if found:
            await answer("**Let's conjugate it...**")
        else:
            await answer("**Nothing found for the given input!**")


"""
These commands will be revamped once libraries with Slash commands support are more stable to work with.
"""

def setup(client) -> None:
    client.add_cog(Language(client))