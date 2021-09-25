import discord
from discord.utils import escape_mentions
from discord.ext import commands

import os
from dotenv import load_dotenv
load_dotenv()

from re import match
from typing import List, Union
import re

guild_ids: List[int] = [int(os.getenv('SERVER_ID'))]
client = commands.Bot(command_prefix='c!', intents=discord.Intents.all(), help_command=None)
cent_id: int = int(os.getenv('CENT_ID'))

@client.event
async def on_ready() -> None:
    """ Tells when the bot is online. """

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

@client.listen(name="on_message")
async def on_message_bot_ping(message):

    author: Union[discord.Member, discord.User] = message.author

    if author.bot:
        return

    if match(f"<@!?{client.user.id}>", message.content) is not None:

        if author.id != cent_id:
            await message.reply(f"**How can I help you my queen, {author.mention}?** 👑")
        else:
            await message.reply(f"**{author.mention}, my prefix is `{client.command_prefix}`**")


@client.listen(name="on_message")
async def on_message_nice_words(message: discord.Message) -> None:
    """ To specific message inputs. """


    regexes: list[str] = [
        r'g{1,99}(0|o){1,99}d{1,99} w{1,99}(0|o){1,99}r[!_\-\w]{0,99}s{0,99}',
        r'c{1,99}(0|o){1,99}l{1,99} w{1,99}(0|o){1,99}r[!_\-\w]{0,99}s{0,99}',
        r'(n|m){1,99}(0|o){0,99}[!_\-\w]{1,99}c[!_\-\w]{1,99} w{1,99}(0|o){0,99}r[!_\-\w]{0,99}s{0,99}'
    ]

    content: str = message.content.lower()
    for regex in regexes:
        found: List[str] = re.findall(regex, content)
        if len(found) <= 0:
            continue

        if content.lower().startswith(found[0]):
            return await message.reply("**I knew you'd say that! 😉🌟**")

@client.command()
async def help(ctx, *, cmd: str =  None):
    """ Shows some information about commands and categories. 
    :param cmd: The command/category. """


    if not cmd:
        embed = discord.Embed(
            title="All commands and categories",
            description=f"```ini\nUse {client.command_prefix}help command or {client.command_prefix}help category to know more about a specific command or category\n\n[Examples]\n[1] Category: {client.command_prefix}help Language\n[2] Command : {client.command_prefix}help word_count```",
            timestamp=ctx.message.created_at,
            color=ctx.author.color
            )

        for cog in client.cogs:
            cog = client.get_cog(cog)
            cog_commands = [c for c in cog.__cog_commands__ if hasattr(c, 'parent') and c.parent is None]
            commands = [f"{client.command_prefix}{c.name}" for c in cog_commands if not c.hidden]
            if commands:
                embed.add_field(
                    name=f"• __{cog.qualified_name}:__",
                    value=f"> {', '.join(commands)}",
                    inline=False
                    )

        cmds = []
        for y in client.walk_commands():
            if not y.cog_name and not y.hidden:
                cmds.append(f"{client.command_prefix}{y.name}")

        embed.add_field(
            name='• __Uncategorized Commands:__',
            value=f"> {', '.join(cmds)}",
            inline=False)
        await ctx.send(embed=embed)

    else:  
        cmd = escape_mentions(cmd)
        if command := client.get_command(cmd.lower()):
            command_embed = discord.Embed(title=f"→ __Command:__ {client.command_prefix}{command.qualified_name}", description=f"__**Description:**__\n```{command.help}```", color=ctx.author.color, timestamp=ctx.message.created_at)
            return await ctx.send(embed=command_embed)

        # Checks if it's a cog
        for cog in client.cogs:
            if str(cog).lower() == str(cmd).lower():
                cog = client.get_cog(cog)
                cog_embed = discord.Embed(title=f"• __Cog:__ {cog.qualified_name}", description=f"__**Description:**__\n```{cog.description}```", color=ctx.author.color, timestamp=ctx.message.created_at)
                cog_commands = [c for c in cog.__cog_commands__ if hasattr(c, 'parent') and c.parent is None]
                commands = [f"{client.command_prefix}{c.name}" for c in cog_commands if not c.hidden]
                if commands:
                    cog_embed.add_field(
                        name=f"→ __Commands:__",
                        value=f"> {', '.join(commands)}",
                        inline=False
                        )
                return await ctx.send(embed=cog_embed)
        # Otherwise, it's an invalid parameter (Not found)
        else:
            await ctx.send(f"**Invalid parameter! It is neither a command nor a cog!**")


for filename in os.listdir('./cogs/'):
    if filename.endswith('.py'):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run(os.getenv('TOKEN'))