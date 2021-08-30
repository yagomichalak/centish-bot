import discord
from discord.ext import commands
import inspect
import io
import textwrap
import traceback
from contextlib import redirect_stdout
from extra import utils

class Tools(commands.Cog):
    """ A category for tool commands. """

    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """ Tells when the Tools cog is ready to go. """

        print('Tools cog is online!')

    @commands.command()
    async def ping(self, ctx):
        """ Show the latency. """

        await ctx.send(f"**:ping_pong: Pong! {round(self.client.latency * 1000)}ms.**")

        # Sends an embedded message
    @commands.command(aliases=['emb'])
    @commands.has_permissions(administrator=True)
    async def embed(self, ctx):
        """ (ADM) Sends an embedded message. """

        await ctx.message.delete()
        if len(ctx.message.content.split()) < 2:
            return await ctx.send('You must inform all parameters!')

        msg = ctx.message.content.split(ctx.message.content.split(' ')[0], 1)
        embed = discord.Embed(description=msg[1], color=ctx.author.color)
        await ctx.send(embed=embed)

    @commands.group(name='post')
    @commands.has_permissions(administrator=True)
    async def _post(self, ctx) -> None:
        """ Posts something. """

        await ctx.message.delete()
        if ctx.invoked_subcommand:
            return

        cmd = self.client.get_command(ctx.command.name)
        prefix = self.client.command_prefix
        subcommands = [f"{prefix}{c.qualified_name}" for c in cmd.commands]

        subcommands = '\n'.join(subcommands)
        embed = discord.Embed(
            title="Subcommads",
            description=f"```apache\n{subcommands}```",
            color=ctx.author.color,
            timestamp=ctx.message.created_at
        )
        await ctx.send(embed=embed)


    
    @_post.command(name="update", aliases=['daily_update', 'du', 'daily'])
    async def _post_update(self, ctx, *, text: str = None) -> None:
        """ Posts a daily update type of message into the channel.
        :param text: The text to post.
        
        PS: The text will be wrapped up in triple tick tags. """

        current_ts = await utils.get_timestamp()

        author = ctx.author

        embed = discord.Embed(
            title="__Daily Update__:",
            description=f"```apache\n{text}```",
            color=1234566,
            timestamp=ctx.message.created_at)
        embed.set_author(name=author, icon_url=author.avatar.url, url=author.avatar.url)

        await ctx.send(content=f"<t:{int(current_ts)}>", embed=embed)

    @_post.command(name="message", aliases=["msg"])
    async def _post_message(self, ctx, title: str = None, *, text: str = None) -> None:
        """ Posts a normal message with title into the channel.
        :param text: The text to post.
        
        PS: The text will be wrapped up in triple tick tags. """

        author = ctx.author

        if not text:
            return await ctx.send(f"**Please, inform a text to send, {author.mention}!**")

        if not title:
            return await ctx.send(f"**Please, inform a title of your message, {author.mention}!**")

        embed = discord.Embed(
            title=f"__{title}__:",
            description=f"```apache\n{text}```",
            color=1234566)

        await ctx.send(embed=embed)

    @commands.group(name='edit')
    @commands.has_permissions(administrator=True)
    async def _edit(self, ctx) -> None:
        """ Edits something. """

        await ctx.message.delete()
        if ctx.invoked_subcommand:
            return

        cmd = self.client.get_command(ctx.command.name)
        prefix = self.client.command_prefix
        subcommands = [f"{prefix}{c.qualified_name}" for c in cmd.commands]

        subcommands = '\n'.join(subcommands)
        embed = discord.Embed(
            title="Subcommads",
            description=f"```apache\n{subcommands}```",
            color=ctx.author.color,
            timestamp=ctx.message.created_at
        )
        await ctx.send(embed=embed)

    @_edit.command(name="message", aliases=['msg'])
    async def _edit_message(self, ctx, message_id: int, *, text: str) -> None:
        """ Edits a bot's message.
        :param message_id: The ID of the message to edit.
        :param text: The new text for that given message. """

        member = ctx.author
        if not message_id:
            return await ctx.send(f"**Please, inform a message ID, {member.mention}!")

        if not text:
            return await ctx.send(f"**Please, inform a text message, {member.mention}!**")

        message = await ctx.channel.fetch_message(message_id)
        if not message:
            return await ctx.send(f"**Invalid message, {member.mention}!**")

        embed = message.embeds[0]
        embed.description = text
        await message.edit(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def eval(self, ctx, *, body: str = None):
        """ (ADM) Executes a given command from Python onto Discord.
        :param body: The body of the command. """
        
        await ctx.message.delete()
        if not body:
            return await ctx.send("**Please, inform the code body!**")

        """Evaluates python code"""
        env = {
            'ctx': ctx,
            'client': self.client,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            'source': inspect.getsource
        }

        def cleanup_code(content):
            """Automatically removes code blocks from the code."""
            # remove ```py\n```
            if content.startswith('```') and content.endswith('```'):
                return '\n'.join(content.split('\n')[1:-1])

            # remove `foo`
            return content.strip('` \n')

        def get_syntax_error(e):
            if e.text is None:
                return f'```py\n{e.__class__.__name__}: {e}\n```'
            return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'

        env.update(globals())

        body = cleanup_code(body)
        stdout = io.StringIO()
        err = out = None

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        def paginate(text: str):
            '''Simple generator that paginates text.'''
            last = 0
            pages = []
            for curr in range(0, len(text)):
                if curr % 1980 == 0:
                    pages.append(text[last:curr])
                    last = curr
                    appd_index = curr
            if appd_index != len(text)-1:
                pages.append(text[last:curr])
            return list(filter(lambda a: a != '', pages))

        try:
            exec(to_compile, env)
        except Exception as e:
            err = await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
            return

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            err = await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            if ret is None:
                if value:
                    try:

                        out = await ctx.send(f'```py\n{value}\n```')
                    except:
                        paginated_text = paginate(value)
                        for page in paginated_text:
                            if page == paginated_text[-1]:
                                out = await ctx.send(f'```py\n{page}\n```')
                                break
                            await ctx.send(f'```py\n{page}\n```')
            else:
                try:
                    out = await ctx.send(f'```py\n{value}{ret}\n```')
                except:
                    paginated_text = paginate(f"{value}{ret}")
                    for page in paginated_text:
                        if page == paginated_text[-1]:
                            out = await ctx.send(f'```py\n{page}\n```')
                            break
                        await ctx.send(f'```py\n{page}\n```')

def setup(client) -> None:
    """ Cog's setup function. """

    client.add_cog(Tools(client))