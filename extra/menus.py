import discord
from discord.ext import commands
from typing import Union, Any, Iterable, Optional


class PaginateView(discord.ui.View):
    """ View for pagination """

    def __init__(self, member: Union[discord.Member, discord.User], items: Iterable[Any], timeout: Optional[float] = None):
        super().__init__(timeout=timeout)
        self.member = member
        self.items = items
        self.index: int = 0


    @discord.ui.button(style=discord.ButtonStyle.success, label="Left", custom_id="go_left_id")
    async def left_page(self, button: discord.ui.button, interaction: discord.Interaction) -> None:

        self.index -= 1
        print(self.index)
        pass

    @discord.ui.button(style=discord.ButtonStyle.success, label="Right", custom_id="go_right_id")
    async def right_page(self, button: discord.ui.button, interaction: discord.Interaction) -> None:

        self.index += 1
        print(self.index)
        pass

    @discord.ui.button(style=discord.ButtonStyle.danger, label="Stop", custom_id="stop_id")
    async def stop_page(self, button: discord.ui.button, interaction: discord.Interaction) -> None:
        
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return self.member.id == interaction.user.id