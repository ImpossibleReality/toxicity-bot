# CSIII Group 3
# Johan N.
# Discord Bot, MongoDB, ZMQ Integration, debugging
# Daniel W.
# Model and debugging, hyperparameter tuning
# Rohan D.
# Math (loss and gradient calculations), data collection and manipulation
# Final Project
# Discord bot which detects and removes toxic messages

import random

import discord
import logging
from discord import app_commands
from discord.ext import tasks
from db import get_config, Config
import time
import os
import prediction
from constants import REPORT_THRESHOLD
from feedback import create_feedback_poll


# Custom Discord.py client (allows for intercepting of messages)
class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.group = app_commands.Group(name="toxicity", description="Manage and Configure Toxicity Bot")
        self.tree = app_commands.CommandTree(self)
        self.tree.add_command(self.group)
        self.server_settings = {}
        self.votes = {}

    # Called when bot is logged in and ready
    async def on_ready(self):
        logging.info('Logged on as {0}!'.format(self.user))

    # Called when the bot intercepts a message
    async def on_message(self, message: discord.Message):
        if message.guild is not None:
            id = message.id
            if not message.channel.permissions_for(message.author).manage_messages or os.environ.get(
                    "IS_TEST").lower() == "true":
                # Predict the message text
                pred = await prediction.predict_text(get_config(message.guild.id).sensitivity, message.content)
                if pred:
                    await (await message.channel.fetch_message(id)).delete()
                    if random.randint(0, 30) == 0:
                        await create_feedback_poll(message.content, message.guild)

    # Called from main method when a message is reported.
    # Increments a running variable for the reports and returns True if that is above the threshold for reporting
    # otherwise returns False
    def report_message(self, msgid: int):
        try:
            self.votes[msgid]['count'] += 1
            self.votes[msgid]['time'] = time.time()
            if self.votes[msgid]['count'] >= REPORT_THRESHOLD:
                return True
        except KeyError:
            # Must create report
            self.votes[msgid] = {
                'count': 1,
                'time': time.time()
            }

    # Gets the cached version of the config for a Discord server
    def get_config(self, id: int) -> Config:
        try:
            # Update time so that cache is not remmoved
            self.server_settings[id]['time'] = time.time()
            return self.server_settings[id]["config"]
        except KeyError:
            # Use DB to get config
            config = get_config(id)
            self.server_settings[id] = {"time": time.time(), "config": config}
            return config

    # Invalidates the config cache for a server
    # Useful in configuration GUI where changes made do configuration should
    # invalidate cache
    def invalidate_config_cache(self, id: int):
        try:
            del self.server_settings[id]
        except KeyError:
            pass

    # Called to setup Discord commands and menus
    async def setup_hook(self):
        # Setup Discord.py command tree and sync it to the Discord API
        await self.tree.sync()

    # Called every 5 minutes to clear the configuration cache
    @tasks.loop(minutes=5)
    async def clear_config_cache(self):
        t = time.time()
        for sid in self.server_settings:
            # If it has been 20 mins or more
            if t - self.server_settings[sid]["time"] > 60 * 20:
                del self.server_settings[sid]

    # Called every 5 mins to clear reports cache
    @tasks.loop(minutes=10)
    async def clear_votes(self):
        t = time.time()
        for sid in self.votes:
            # If the time is more than an hour
            if t - self.votes[sid]["time"] > 60 * 60:
                del self.votes[sid]
