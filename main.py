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
from typing import Any, List, Dict, Union

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

    if message.content.lower().startswith('nice words'):
        await message.reply("**I knew you'd say that! 😉🌟**")


    await client.process_commands(message)


@tasks.loop(seconds=30)
async def change_bot_status():

    words = await Centish.get_words()
    random_word = choice(words['words'])
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, 
            name=f"{random_word['word']} | {random_word['translation']}"))

@client.command()
async def test(ctx) -> None:
    await ctx.reply("**Command successfully tested!**")


@client.slash_command(guild_ids=guild_ids)  # create a slash command for the supplied guilds
async def hello(ctx):
    """Say hello to the bot"""  # the command description can be supplied as the docstring
    await ctx.send(f"Hello {ctx.author}!")

for filename in os.listdir('./cogs/'):
    if filename.endswith('.py'):
        client.load_extension(f"cogs.{filename[:-3]}")



@client.user_command(name="pat", guild_ids=guild_ids)
async def _pat(ctx, user: discord.Member) -> None:
    """ Pats someone. """

    await ctx.send(f"**{ctx.author.mention} patted {user.mention}!**")

# Slash commands
@client.slash_command(name="words", guild_ids=guild_ids)
async def _words_slash(ctx,
    word_type: Option(str, name="word_type", description="The type of word", required=False, choices=[
        "Adverb", "Verb", "Adjective", "Noun", "Determiner",
        "Predeterminer", "Exclamation", "Question", "Conjunction",
        "Preposition"
    ])) -> Any:
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

    def find_words(search, words) -> List[Dict[str, Any]]:
        """ Finds the word in the strings """
        found = []
        for word in words['words']:
            
            searchable_columns = ' '.join([word['word'].lower(), word['translation'].lower()])
            idx = searchable_columns.find(search)
            if idx != -1:
                found.append(word)

        return found

    words = await Centish.get_words()
    found = find_words(search, words)

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


client.run(os.getenv('TOKEN'))