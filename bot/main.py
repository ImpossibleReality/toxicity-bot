import os

import discord
from discord import app_commands
from dotenv import load_dotenv

from bot import MyClient
from config_gui import create_config_gui
from db import connect
import prediction

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
    e, v = create_config_gui(interaction.guild_id, client)
    await interaction.response.send_message(embed=e,view=v)
    v.message = await interaction.original_message()

@client.tree.context_menu(name="Flag as toxic")
async def flag_msg(interaction: discord.Interaction, message: discord.Message):
    """Flag a Discord message as toxic"""
    await interaction.response.send_message("Flagged", ephemeral=True)


connect()
client.run(os.environ.get("BOT_TOKEN"))
