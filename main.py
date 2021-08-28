import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
load_dotenv()
import os
from extra.language.centish import Centish
from random import choice

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


for filename in os.listdir('./cogs/'):
    if filename.endswith('.py'):
        client.load_extension(f"cogs.{filename[:-3]}")


client.run(os.getenv('TOKEN'))