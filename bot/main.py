from dotenv import load_dotenv
import discord
from discord import app_commands
import os
from config_gui import create_config_gui
from bot import MyClient
from db import connect

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)


@client.group.command()
@app_commands.describe(
    message="Message to return probability for"
)
async def toxicity_prob(interaction: discord.Interaction, message: str):
    """Returns a probability between 0 and 1 of how toxic a message is deemed to be."""
    await interaction.response.send_message("Probability: NOT IMPLEMENTED", ephemeral=True)

@client.group.command()
async def config(interaction: discord.Interaction):
    """Configure Toxicity Bot"""
    e, v = create_config_gui(interaction.guild_id)
    await interaction.response.send_message(embed=e,view=v)

connect()
client.run(os.environ.get("BOT_TOKEN"))
