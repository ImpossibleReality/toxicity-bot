import coloredlogs
import logging

import os

from bot import MyClient
from bot.feedback import create_feedback_poll
from config_gui import create_config_gui
from db import connect
import prediction

import discord
from discord import app_commands
from dotenv import load_dotenv

coloredlogs.install()

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)


@client.group.command()
@app_commands.describe(
    message="Message to return probability for"
)
async def probability(interaction: discord.Interaction, message: str):
    """Returns a probability between 0 and 1 of how toxic a message is deemed to be."""
    prob = await prediction.predict_text_prob(interaction.client.get_config(interaction.guild_id).sensitivity, message)
    await interaction.response.send_message("Probability: " + str(prob), ephemeral=True)


@client.group.command()
async def config(interaction: discord.Interaction):
    """Configure Toxicity Bot"""
    e, v = create_config_gui(interaction.guild_id, client, interaction)
    await interaction.response.send_message(embed=e, view=v)
    v.message = await interaction.original_message()


@client.tree.context_menu(name="Flag as toxic")
@app_commands.checks.cooldown(1, 600, key=lambda i: (i.guild_id, i.user.id))
async def flag_msg(interaction: discord.Interaction, message: discord.Message):
    """Flag a Discord message as toxic"""
    if client.report_message(message.id):
        await create_feedback_poll(message.content, interaction.guild)
    await interaction.response.send_message("Flagged", ephemeral=True)


@flag_msg.error
async def on_test_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message("You cannot flag messages this fast.", ephemeral=True)


connect()
logging.info("Connected to DB.")
logging.info("Connecting to discord...")
client.run(os.environ.get("BOT_TOKEN"), log_handler=None)
