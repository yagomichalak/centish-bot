import discord
from discord.ext import commands, tasks
from discord.app.commands import user_command, message_command, slash_command, Option
from typing import Optional, List, Dict, Union
import os

from extra.language.centish import Centish
from extra.menus import WordPaginationView, ConjugationView
from extra import utils
from random import choice

guild_ids: List[int] = [int(os.getenv('SERVER_ID'))]

class Language(commands.Cog, Centish):
    """ Category for commands related to the Centish language. """

    def __init__(self, client) -> None:
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """ Tells when the cog is ready to go. """

        self.change_bot_status.start()

        print('Language cog is online!')

    @tasks.loop(seconds=30)
    async def change_bot_status(self):

        words = await Centish.get_words()
        random_word = choice(words['words'])
        await self.client.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, 
                name=f"{random_word['word']} | {random_word['translation']}"))

    @commands.command(name="word_count", aliases=['wc', "words_count", "count_words"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _word_count_command(self, ctx) -> None:
        """ Tells how many words there are currently in the Centish language. """

        await self._word_count(ctx)

    
    @slash_command(name="word_count", guild_ids=guild_ids)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _word_count_slash(self, ctx) -> None:
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
        """ Shows Centish words.

        :param word_type: The type of word to show. [Optional][Default=All] """

        await self._words(ctx, word_type)

    @slash_command(name="words", guild_ids=guild_ids)
    async def _words_slash(self, ctx,
        word_type: Option(str, name="word_type", description="The type of word", required=False, choices=[
            "Adverb", "Verb", "Adjective", "Noun", "Determiner",
            "Predeterminer", "Exclamation", "Question", "Conjunction",
            "Preposition"
        ])) -> None:
        """ Shows Centish words.

            :param word_type: The type of word to show. [Optional][Default=All] """

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

        msg = await answer("\u200b", embed=embed, view=view)

        await view.wait()
        await utils.disable_buttons(view)
        await msg.edit(view=view)



    @slash_command(name="find", guild_ids=guild_ids)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _find(self, ctx, search: Option(str, description="The word to search for.", required=True)) -> None:
        """ Finds words based on a search. """

        member = ctx.author
        await ctx.defer()

        words = await Centish.get_words()
        found = await Centish.find_words(search, words['words'])

        if not found:
            return await ctx.followup.send(f"**Nothing found for the given search, {member.mention}!**")
        
        data: Dict[str, Union[str, List[Dict[str, Union[str, List[str]]]]]] = {
            'word_type': search,
            'words': found
        }

        # Paginates word list
        view = WordPaginationView(member, data)
        embed = await view.get_page()

        msg = await ctx.followup.send("\u200b", embed=embed, view=view)

        await view.wait()
        await utils.disable_buttons(view)
        await msg.edit(view=view)


    @slash_command(name="conjugate", guild_ids=guild_ids)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _conjugate_command(self, ctx, 
        verb: Option(str, description="The verb to conjugate.", required=True)) -> None:
        """ Conjugates a verb in Centish.
        :param verb: The verb to conjugate. """

        await ctx.defer()
        await self._conjugate_callback(ctx, verb)

    async def _conjugate_callback(self, ctx, verb: str) -> None:
        """ Conjugates a verb in Centish.
        :param verb: The verb to conjugate. """

        author = ctx.author

        answer: discord.PartialMessageable = ctx.send if isinstance(ctx, commands.Context) else ctx.followup.send

        words = await Centish.get_words()
        filtered_words = await Centish.filter_words(words['words'], 'verb')
        found = await Centish.find_words(verb, filtered_words, multiple=False)
        tenses = await Centish.get_tenses()


        if not found:
            return await answer("**Nothing found for the given input!**")

        data = {
            'words': filtered_words,
            'verb': found,
            'tenses': tenses
        }
        view = ConjugationView(member=author, data=data, timeout=60)
        embed = await view.start()
        msg = await answer("\u200b", embed=embed, view=view)
        await view.wait()
        await utils.disable_buttons(view)
        await msg.edit(view=view)

def setup(client) -> None:
    client.add_cog(Language(client))