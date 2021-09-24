import discord
from discord.ext import commands
from discord.app.commands import slash_command, Option, OptionChoice

import inspect
import io
import textwrap
import traceback
from contextlib import redirect_stdout

from extra import utils
from typing import List, Dict, Union
import os

guild_ids: List[int] = [int(os.getenv('SERVER_ID'))]
updates_role_id: int = int(os.getenv('UPDATES_ROLE_ID'))

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

    @slash_command(name="embed", default_permission=False, guild_ids=guild_ids)
    @commands.has_permissions(administrator=True)
    async def _embed(self, ctx,
        description: Option(str, name="description", description="Description.", required=False),
        title: Option(str, name="title", description="Title.", required=False),
        timestamp: Option(bool, name="timestamp", description="If timestamp is gonna be shown.", required=False),
        url: Option(str, name="url", description="URL for the title.", required=False),
        thumbnail: Option(str, name="thumbnail", description="Thumbnail for the embed.", required=False),
        image: Option(str, name="image", description="Display image.", required=False),
        color: Option(str, name="color", description="The color for the embed.", required=False,
            choices=[
                OptionChoice(name="Blue", value="0011ff"), OptionChoice(name="Red", value="ff0000"),
                OptionChoice(name="Green", value="00ff67"), OptionChoice(name="Yellow", value="fcff00"),
                OptionChoice(name="Black", value="000000"), OptionChoice(name="White", value="ffffff"),
                OptionChoice(name="Orange", value="ff7100"), OptionChoice(name="Brown", value="522400"),
                OptionChoice(name="Purple", value="380058")])) -> None:
        """ (ADM) Makes an improved embedded message """

        await ctx.delete()

        # Checks if there's a timestamp and sorts time
        embed = discord.Embed()

        # Adds optional parameters, if informed
        if title: embed.title = title
        if timestamp: embed.timestamp = await utils.parse_time()
        if description: embed.description = description.replace(r'\n', '\n')
        if color: embed.color = int(color, 16)
        if thumbnail: embed.set_thumbnail(url=thumbnail)
        if url: embed.url = url


        files = []

        if image and image.startswith('attachment://'):
            filename = image.replace('attachment://', '')

            embed.set_image(url=f"attachment://{filename}")
            files.append(discord.File(f"./media/images/{filename}", filename=filename))

        elif image:
            embed.set_image(url=image)

        if thumbnail and thumbnail.startswith('attachment://'):
            filename = thumbnail.replace('attachment://', '')
            
            embed.set_thumbnail(url=f"attachment://{filename}")
            files.append(discord.File(f"./media/images/{filename}", filename=filename))


        if not description and not image and not thumbnail:
            return await ctx.respond(
                f"**{ctx.author.mention}, you must inform at least one of the following options: `description`, `image`, `thumbnail`**")

        await ctx.channel.send("\u200b", embed=embed, files=files)

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

        updates_role = discord.utils.get(ctx.guild.roles, id=updates_role_id)
        await ctx.send(content=f"{updates_role.mention}, <t:{int(current_ts)}>", embed=embed)

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

    @_post.command(name="info_messages", aliases=['info_msgs', 'info', 'information'])
    async def _information_messages(self, ctx) -> None:
        """ Posts all information messages embedded neatly. """

        infos: Dict[str, Dict[str, Union[str, int, discord.Color]]] = {
            "italian": {"title": "informazione", "name": "italiano", "emoji": "🇮🇹", "color": 1234566, "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Flag_of_Italy.svg/2560px-Flag_of_Italy.svg.png", "message": None},
            "french": {"title": "information", "name": "français", "emoji": "🇫🇷", "color": int(discord.Color.blue()), "image": "https://upload.wikimedia.org/wikipedia/commons/6/62/Flag_of_France.png", "message": None},
            "portuguese": {"title": "informação", "name": "português", "emoji": "🇧🇷", "color": int(discord.Color.gold()), "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Flag_of_Brazil.svg/1024px-Flag_of_Brazil.svg.png", "message": None},
            "english": {"title": "information", "name": "english", "emoji": "🇺🇸", "color": int("ffffff", 16), "image": "https://cdn.britannica.com/79/4479-050-6EF87027/flag-Stars-and-Stripes-May-1-1795.jpg", "message": None},
            "centish": {"title": "informazza", "name": "cajdklaje", "emoji": "☪️", "color": int(discord.Color.purple()), "image": "https://images.emojiterra.com/twitter/v13.0/512px/262a.png", "message": None}
        }

        # Posting all information channels.
        for language, info in infos.items():
            with open(f"./media/texts/information/{language}.txt", encoding="utf-8") as file:
                language_text = file.read()

                info_embed = discord.Embed(
                    title=f"{info['emoji']} __{info['title'].title()}__ {info['emoji']} ({info['name'].title()})",
                    description=language_text,
                    color=info['color'],
                    timestamp=ctx.message.created_at
                )

                info_embed.set_image(url="attachment://banner.png")
                info_embed.set_thumbnail(url=info['image'])
                info_embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon.url)
                f = discord.File("media/images/cajdklaje_banner.png", filename="banner.png")
                msg = await ctx.send(embed=info_embed, file=f)
                info['message'] = msg.jump_url

        # Makes a menu link containing jump to message buttons
        view = discord.ui.View()
        menu_embed = discord.Embed(
            title="__**Informazza Linkror**__ ☪️",
            description="Click in any of the buttons below to get redirect to the **information** message written in your language.",
            color=discord.Color.dark_blue()
        )
        view = discord.ui.View()
        for info in infos.values():
            view.add_item(discord.ui.Button(emoji=info['emoji'], label=info['name'].title(), url=info['message']))
        await ctx.send("\u200b", embed=menu_embed, view=view)

    @_post.command(name="language_messages", aliases=['lang_msgs', 'lang', 'language', 'languages'])
    async def _language_messages(self, ctx) -> None:
        """ Posts all information messages embedded neatly. """

        infos: Dict[str, Dict[str, Union[str, int, discord.Color]]] = {
            "italian": {"title": "la lingua", "name": "italiano", "emoji": "🇮🇹", "color": 1234566, "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Flag_of_Italy.svg/2560px-Flag_of_Italy.svg.png", "message": None},
            "french": {"title": "la langue", "name": "français", "emoji": "🇫🇷", "color": int(discord.Color.blue()), "image": "https://upload.wikimedia.org/wikipedia/commons/6/62/Flag_of_France.png", "message": None},
            "portuguese": {"title": "a língua", "name": "português", "emoji": "🇧🇷", "color": int(discord.Color.gold()), "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Flag_of_Brazil.svg/1024px-Flag_of_Brazil.svg.png", "message": None},
            "english": {"title": "the language", "name": "english", "emoji": "🇺🇸", "color": int("ffffff", 16), "image": "https://cdn.britannica.com/79/4479-050-6EF87027/flag-Stars-and-Stripes-May-1-1795.jpg", "message": None},
            "centish": {"title": "klaje", "name": "cajdklaje", "emoji": "☪️", "color": int(discord.Color.purple()), "image": "https://images.emojiterra.com/twitter/v13.0/512px/262a.png", "message": None}
        }

        # Posting all information channels.
        for language, info in infos.items():
            with open(f"./media/texts/language/{language}.txt", encoding="utf-8") as file:
                language_text = file.read()

                info_embed = discord.Embed(
                    title=f"{info['emoji']} __{info['title'].title()}__ {info['emoji']} ({info['name'].title()})",
                    description=language_text,
                    color=info['color'],
                    timestamp=ctx.message.created_at
                )

                info_embed.set_image(url="attachment://banner.png")
                info_embed.set_thumbnail(url=info['image'])
                info_embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon.url)
                f = discord.File("media/images/cajdklaje_banner.png", filename="banner.png")
                msg = await ctx.send(embed=info_embed, file=f)
                info['message'] = msg.jump_url

        # Makes a menu link containing jump to message buttons
        view = discord.ui.View()
        menu_embed = discord.Embed(
            title="__**Klaje Linkror**__ ☪️",
            description="Click in any of the buttons below to get redirect to the **language** message written in your language.",
            color=discord.Color.dark_blue()
        )
        view = discord.ui.View()
        for info in infos.values():
            view.add_item(discord.ui.Button(emoji=info['emoji'], label=info['name'].title(), url=info['message']))
        await ctx.send("\u200b", embed=menu_embed, view=view)


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
        if message is None:
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