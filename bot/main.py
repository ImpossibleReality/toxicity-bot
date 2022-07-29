# CSIII Group 3
# Johan N.
# Discord Bot, MongoDB, ZMQ Integration, debugging
# Daniel W.
# Model and debugging, hyperparameter tuning
# Rohan D.
# Math (loss and gradient calculations), data collection and manipulation
# Final Project
# Discord bot which detects and removes toxic messages

import coloredlogs
import logging

import os

from bot import MyClient
from bot.feedback import create_feedback_poll
from config_gui import create_config_gui
from db import connect, get_config
import prediction

import discord
from discord import app_commands
from dotenv import load_dotenv

# Use colored logging because it looks better
coloredlogs.install()

# Load env vars from .env file
load_dotenv()

# Create custom client from __init__.py file
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)


# Debug command which returns the probability and cutoff of a message being flagged
# Using the server's model
@client.group.command()
@app_commands.describe(
    message="Message to return probability for"
)
async def probability(interaction: discord.Interaction, message: str):
    """Returns a probability between 0 and 1 of how toxic a message is deemed to be."""
    prob = await prediction.predict_text_prob(interaction.client.get_config(interaction.guild_id).sensitivity, message)
    await interaction.response.send_message("Probability: " + str(prob), ephemeral=True)

# Command which allows for configuring of the bot
@client.group.command()
async def config(interaction: discord.Interaction):
    """Configure Toxicity Bot"""
    e, v = create_config_gui(interaction.guild_id, client, interaction)
    await interaction.response.send_message(embed=e, view=v)
    v.message = await interaction.original_message()

# Context menu command to report a message
@client.tree.context_menu(name="Flag as toxic")
@app_commands.checks.cooldown(1, 600, key=lambda i: (i.guild_id, i.user.id))
async def flag_msg(interaction: discord.Interaction, message: discord.Message):
    """Flag a Discord message as toxic"""
    c = get_config(interaction.guild_id)
    if not c.reporting:
        await interaction.response.send_message("Flagging is disabled on your server.", ephemeral=True)
        return

    if client.report_message(message.id):
        await create_feedback_poll(message.content, interaction.guild)
    await interaction.response.send_message("Flagged", ephemeral=True)

# Function to be called when the user is on cooldown for the reporting feature
@flag_msg.error
async def on_test_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message("You cannot flag messages this fast.", ephemeral=True)

# Connect to DB
logging.info("Connected to DB.")
connect()

# Connect to Discord and run the bot
logging.info("Connecting to discord...")
client.run(os.environ.get("BOT_TOKEN"), log_handler=None)
