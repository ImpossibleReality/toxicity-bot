import discord
import logging
from discord import app_commands
from discord.ext import tasks
from db import get_config, Config
import time
import os
import prediction

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.group = app_commands.Group(name="toxicity", description="Manage and Configure Toxicity Bot")
        self.tree = app_commands.CommandTree(self)
        self.tree.add_command(self.group)
        self.server_settings = {}
    async def on_ready(self):
        logging.info('Logged on as {0}!'.format(self.user))

    async def on_message(self, message: discord.Message):
        if message.guild is not None:
            if not message.channel.permissions_for(message.author).manage_messages or os.environ.get(
                    "IS_TEST").lower() == "true":
                pred = await prediction.predict_text(get_config(message.guild.id).sensitivity, message.content)
                print(pred)
                if pred:
                    await message.delete()

    def get_config(self, id: int) -> Config:
        try:
            self.server_settings[id]['time'] = time.time()
            return self.server_settings[id]["config"]
        except KeyError:
            config = get_config(id)
            self.server_settings[id] = {"time": time.time(), "config": config}
            return config

    def invalidate_config_cache(self, id: int):
        try:
            del self.server_settings[id]
        except KeyError:
            pass

    async def setup_hook(self):
        await self.tree.sync()

    @tasks.loop(minutes=5)
    async def clear_config_cache(self):
        t = time.time()
        for sid in self.server_settings:
            if t - self.server_settings[sid]["time"] > 60 * 20:
                del self.server_settings[sid]