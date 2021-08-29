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

    @commands.command(aliases=['wc'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def words_count(self, ctx) -> None:
        """ Tells how many words there are currently in the Centish language. """

        words = await self.get_words()
        await ctx.send(
            f"**There are currently `{len(words['words'])}` words in the `Centish` language, {ctx.author.mention}!**")

    
    @commands.group()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def words(self, ctx, word_type: Optional[str] = None) -> None:
        """ Shows Centish words.

        :param word_type: The type of word to show. [Optional][Default=All] """

        author = ctx.author

        accepted_word_types: List[str] = [
            'adjective', 'noun', 'adverb', 'verb', 'exclamation', 
            'question', 'pronoun', 'conjunction', 'preposition'
        ]

        if word_type:
            if word_type.lower() not in accepted_word_types:
                return await ctx.send(f"**Please, inform a valid `word type`, {author.mention}!**\n{', '.join(accepted_word_types)}")

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

        msg = await ctx.send(embed=embed, view=view)

        await view.wait()

        await utils.disable_buttons(view)
        await msg.edit(view=view)
        

        



"""
These commands will be revamped once libraries with Slash commands support are more stable to work with.
"""

def setup(client) -> None:
    client.add_cog(Language(client))