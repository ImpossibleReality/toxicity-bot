# CSIII Group 3
# Johan N.
# Discord Bot, MongoDB, ZMQ Integration, debugging
# Daniel W.
# Model and debugging, hyperparameter tuning
# Rohan D.
# Math (loss and gradient calculations), data collection and manipulation
# Final Project
# Discord bot which detects and removes toxic messages

import discord
from db import get_config, create_feedback, has_voted, update_feedback_counts


# Button for voting on a feedback poll
class VoteButton(discord.ui.Button):
    def __init__(self, isGood: bool):
        self.isGood = isGood
        if isGood:
            super().__init__(style=discord.ButtonStyle.green, label="Appropriate")
        else:
            super().__init__(style=discord.ButtonStyle.danger, label="Innapropriate")

    async def callback(self, interaction: discord.Interaction):
        msgid = interaction.message.id
        if has_voted(msgid, interaction.user.id):
            # User has already voted
            await interaction.response.send_message("You have already voted!", ephemeral=True)
            return

        # Update feedback counts
        update_feedback_counts(msgid, self.isGood, interaction.user.id)
        await interaction.response.send_message("Voting successful.", ephemeral=True)


# Main view for feedback poll
class FeedbackView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(VoteButton(True))
        self.add_item(VoteButton(False))

# Create a new feedback poll in a guild using the feedback channel if one exists
async def create_feedback_poll(message: str, guild: discord.Guild):
    c = get_config(guild.id)
    if c.feedback_channel is None:
        return
    channel = guild.get_channel(c.feedback_channel)
    if channel is None:
        return
    v = FeedbackView()

    # Show the message in a spoiler
    e = discord.Embed(colour=discord.Color.random(), title="Give feedback", description="Message: ||" + message + "||")
    poll_message = await channel.send(view=v, embed=e)
    create_feedback(guild.id, message, c.sensitivity, poll_message.id)
