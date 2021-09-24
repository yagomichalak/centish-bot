import discord
from discord.ext import commands
import asyncio
from typing import Union, List, Any

class ConfirmButton(discord.ui.View):
	""" Button class for asking members for confirmation. """

	def __init__(self, member: Union[discord.User, discord.Member], timeout: int = 180) -> None:
		super().__init__(timeout=timeout)
		self.member = member
		self.value = None

	@discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
	async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
		""" Confirms the prompt. """

		self.value = True
		self.stop()

	# This one is similar to the confirmation button except sets the inner value to `False`
	@discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
	async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
		""" Cancels the prompt. """

		self.value = False
		self.stop()

	async def interaction_check(self, interaction: discord.Interaction) -> bool:
		""" Checks whether user can interact with the view and its buttons. """

		return self.member.id == interaction.user.id


class ValueButton(discord.ui.Button):
	""" Button class for returning a number value. """

	async def callback(self, interaction: discord.Interaction) -> None:

		self.view.value = self.view.children.index(self)
		self.view.stop()

