import discord
from discord.ext import commands
from extra.language.centish import Centish
from typing import Optional, List
from extra.menus import PaginateView

class Language(commands.Cog, Centish):
    """ Category for commands related to the Centish language. """

    def __init__(self, client) -> None:
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """ Tells when the cog is ready to go. """

        print('Language cog is online!')

    
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


        index = 0
        words = words[index:index+15]
        
        
        # Creates basic embed
        embed = discord.Embed(
            title=f"__Showing Words__: ({word_type.title()})",
            color=author.color,
            timestamp=ctx.message.created_at
        )

        # Makes header
        temp_text1 = f"{'[Word]':^12} | {'[Translation]':<13} | {'[Types]':^15}"
        embed.add_field(
            name=f"{'='*50}",
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
            name=f"{'='*50}",
            value=f"```apache\n{formatted_words}```",
            inline=False
        )

        # Paginates word list
        view = PaginateView(author, words)
        msg = await ctx.send(embed=embed, view=view)

        await view.wait()
        
        await ctx.send("Ahh")
        

        



"""
These commands will be revamped once libraries with Slash commands support are more stable to work with.
"""

def setup(client) -> None:
    client.add_cog(Language(client))