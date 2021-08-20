import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
import os

client = commands.Bot(command_prefix='c!', intents=discord.Intents.all())

@client.event
async def on_ready() -> None:
    """ Tells when the bot is online. """

@client.command()
async def test(ctx) -> None:
    await ctx.reply("**Command successfully tested!**")


for filename in os.listdir('./cogs/'):
    if filename.endswith('.py'):
        client.load_extension(f"cogs.{filename[:-3]}")


client.run(os.getenv('TOKEN'))