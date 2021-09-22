import discord
from discord.app.commands import Option
from discord.ext import commands, tasks
from dotenv import load_dotenv
load_dotenv()
import os
from extra.language.centish import Centish
from extra.menus import WordPaginationView
from extra import utils
from random import choice
from typing import List, Dict, Union
import re

guild_ids: List[int] = [int(os.getenv('SERVER_ID'))]
client = commands.Bot(command_prefix='c!', intents=discord.Intents.all())

@client.event
async def on_ready() -> None:
    """ Tells when the bot is online. """

    change_bot_status.start()
    print('Bot is ready!')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You can't do that!")

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please, inform all parameters!')

    elif isinstance(error, commands.NotOwner):
        await ctx.send("You're not the bot's owner!")

    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(error)

    elif isinstance(error, commands.MissingAnyRole):
        role_names = [f"**{str(discord.utils.get(ctx.guild.roles, id=role_id))}**" for role_id in error.missing_roles]
        await ctx.send(f"You are missing at least one of the required roles: {', '.join(role_names)}")

    elif isinstance(error, commands.errors.RoleNotFound):
        await ctx.send(f"**{error}**")

    elif isinstance(error, commands.ChannelNotFound):
        await ctx.send("**Channel not found!**")

    print('='*10)
    print(f"ERROR: {error} | Class: {error.__class__} | Cause: {error.__cause__}")
    print('='*10)

@client.event
async def on_message(message: discord.Message) -> None:
    """ To specific message inputs. """


    regexes: list[str] = [
        r'g{1,99}o{2,99}d{1,99} w{1,99}o{1,99}r[!_\-\w]s{0,99}',
        r'c{1,99}o{2,99}l{1,99} w{1,99}o{1,99}r[!_\-\w]s{0,99}',
        r'(n|m){1,99}[!_\-\w]{1,99}c[!_\-\w]{1,99} w{1,99}o{1,99}r[!_\-\w]{1,99}s{0,99}'
    ]

    content: str = message.content.lower()
    for regex in regexes:
        found: List[str] = re.findall(regex, content)
        if len(found) <= 0:
            continue

        if content.lower().startswith(found[0]):
            return await message.reply("**I knew you'd say that! 😉🌟**")


    await client.process_commands(message)


@tasks.loop(seconds=30)
async def change_bot_status():

    words = await Centish.get_words()
    random_word = choice(words['words'])
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, 
            name=f"{random_word['word']} | {random_word['translation']}"))

for filename in os.listdir('./cogs/'):
    if filename.endswith('.py'):
        client.load_extension(f"cogs.{filename[:-3]}")

@client.user_command(name="Pat", guild_ids=guild_ids)
async def _pat(ctx, user: discord.Member) -> None:
    """ Pats someone. """

    await ctx.respond(f"**{ctx.author.mention} patted {user.mention}!**")

@client.user_command(name="Kiss", guild_ids=guild_ids)
async def _kiss(ctx, user: discord.Member) -> None:
    """ Kisses someone. """

    author = ctx.author
    if user == author:
        return await ctx.respond(f"**You cannot kiss yourself, lol!**", ephemeral=True)

    if user.bot:
        return await ctx.respond("**You cannot kiss a bot!**", ephemeral=True)

    embed = discord.Embed(
        title="__Kiss__",
        description=f"💓 **{ctx.author.mention} kissed {user.mention}!** 💓",
        color=discord.Color.brand_red()
    )

    kisses: List[str] = [
            'https://c.tenor.com/sx0mJIjy61gAAAAC/milk-and-mocha-bear-couple.gif',
            'https://c.tenor.com/hK8IUmweJWAAAAAC/kiss-me-%D0%BB%D1%8E%D0%B1%D0%BB%D1%8E.gif',
            'https://c.tenor.com/Aaxuq2evHe8AAAAC/kiss-cute.gif',
            'https://c.tenor.com/A0ixOj7Y1WUAAAAC/kiss-anime.gif',
            'https://c.tenor.com/ErAPuiWY46QAAAAC/kiss-anime.gif',
            'https://c.tenor.com/4GdkzkTQdI8AAAAC/kissing-love.gif',
            'https://c.tenor.com/lsOkG57_ibIAAAAd/kiss-lip-kiss.gif',
            'https://c.tenor.com/uF0-jdZRkLYAAAAC/kissing-kiss.gif',
            'https://c.tenor.com/3kvvlXjRse0AAAAC/kiss-lip-kiss.gif',
            'https://c.tenor.com/RZEZVjS3MeMAAAAC/forcibly-kissing-deep-kiss.gif',
            'https://c.tenor.com/teTesMTK_c4AAAAC/shiksha-wedding.gif',
            'https://c.tenor.com/RrUKz9kC3bUAAAAi/dovey-bunnies-kisses.gif',
            'https://c.tenor.com/FDcq03ZLNX0AAAAi/love-couple.gif',
            'https://c.tenor.com/LbOTuZXj9y4AAAAC/cat-love.gif',
            'https://c.tenor.com/OhTr6EO7u14AAAAC/love-you-kiss.gif',
            'https://c.tenor.com/xTSmPl72UjYAAAAC/kiss-blushing.gif',
            'https://c.tenor.com/Gr8BaRWOudkAAAAC/brown-and-cony-kiss.gif',
            'https://c.tenor.com/uhB9b3AzxrQAAAAC/brown.gif',
            'https://c.tenor.com/cK2c6eQ7Is8AAAAC/cony-and-brown-hug.gif',
            'https://c.tenor.com/sXNJMF5vI8oAAAAC/love-peachcat.gif',
            'https://c.tenor.com/MXd8Xby7jnMAAAAC/davydoff-love.gif',
            'https://c.tenor.com/yWGhrAd0cioAAAAC/kissing-couple.gif'

        ]

    embed.set_author(name=author, icon_url=author.display_avatar)
    embed.set_image(url=choice(kisses))
    embed.set_footer(text=user, icon_url=user.display_avatar)

    await ctx.respond(embed=embed)

# Slash commands
@client.slash_command(name="words", guild_ids=guild_ids)
async def _words_slash(ctx,
    word_type: Option(str, name="word_type", description="The type of word", required=False, choices=[
        "Adverb", "Verb", "Adjective", "Noun", "Determiner",
        "Predeterminer", "Exclamation", "Question", "Conjunction",
        "Preposition"
    ])) -> None:
    """ Shows Centish words.

        :param word_type: The type of word to show. [Optional][Default=All] """

    await client.get_cog('Language')._words(ctx, word_type)


@client.slash_command(name="word_count", guild_ids=guild_ids)
@commands.cooldown(1, 5, commands.BucketType.user)
async def _word_count_slash(ctx) -> None:
    """ Tells how many words there are currently in the Centish language. """

    await client.get_cog('Language')._word_count(ctx)

@client.slash_command(name="find", guild_ids=guild_ids)
@commands.cooldown(1, 5, commands.BucketType.user)
async def _find(ctx, search: Option(str, description="The word to search for.", required=True)) -> None:
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

    msg = await ctx.followup.send(embed=embed, view=view)

    await view.wait()
    await utils.disable_buttons(view)
    await msg.edit(view=view)


@client.slash_command(name="conjugate", guild_ids=guild_ids)
@commands.cooldown(1, 5, commands.BucketType.user)
async def _conjugate_command(ctx, 
    verb: Option(str, description="The verb to conjugate.", required=True)) -> None:
    """ Conjugates a verb in Centish.
    :param verb: The verb to conjugate. """

    await ctx.defer()
    await client.get_cog('Language')._conjugate_callback(ctx, verb)


client.run(os.getenv('TOKEN'))