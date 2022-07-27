import discord
import logging
from discord import app_commands
import os


def is_bad(message: str):
    return "idiot" in message

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.group = app_commands.Group(name="toxicity", description="Manage and Configure Toxicity Bot")
        self.tree = app_commands.CommandTree(self)
        self.tree.add_command(self.group)
    async def on_ready(self):
        logging.info('Logged on as {0}!'.format(self.user))

    async def on_message(self, message: discord.Message):
        if not message.channel.permissions_for(message.author).manage_messages or os.environ.get(
                "IS_TEST").lower() == "true":
            if is_bad(message.content):
                await message.delete()

    async def setup_hook(self):
        await self.tree.sync()
