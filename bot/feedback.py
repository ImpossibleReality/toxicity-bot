import discord
from db import get_config, create_feedback, has_voted, update_feedback_counts

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
            await interaction.response.send_message("You have already voted!", ephemeral=True)
            return
        update_feedback_counts(msgid, self.isGood, interaction.user.id)
        await interaction.response.send_message("Voting successful.", ephemeral=True)


class ConfigView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(VoteButton(True))
        self.add_item(VoteButton(False))



async def create_feedback_poll(message: str, guild: discord.Guild):
    c = get_config(guild.id)
    if c.feedback_channel is None:
        return
    channel = guild.get_channel(c.feedback_channel)
    if channel is None:
        return
    v = ConfigView()
    e = discord.Embed(colour=discord.Color.random(), title="Give feedback", description="Message: ||" + message + "||")
    poll_message = await channel.send(view=v, embed=e)
    create_feedback(guild.id, message, c.sensitivity, poll_message.id)