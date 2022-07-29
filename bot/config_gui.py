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

from bot import MyClient
from db import Config, get_config, set_config


# Allows user to select the model/sensitivity used in that server
class SensitivityDropdown(discord.ui.Select):
    def __init__(self, config: Config, client: MyClient, interaction: discord.Interaction):
        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label='Loose', description='Flags only severe hate speech and profanity', emoji='🟢',
                                 default=config.sensitivity == 0, value="0"),
            discord.SelectOption(label='Moderate', description='Flags moderate hate speech and profanity', emoji='🟠',
                                 default=config.sensitivity == 1, value="1"),
            discord.SelectOption(label='Strict', description='Flags mild profanity and all hate speech', emoji='🔴',
                                 default=config.sensitivity == 2, value="2"),
        ]

        self.interaction = interaction
        self.config = config
        self.client = client

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Sensitivity', min_values=1, max_values=1, options=options,
                         custom_id="config_select")

    # Called when the user selects an item in the dropdown
    async def callback(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            # User is not administrator, notify them and return from the function
            await interaction.response.send_message("You are not an administrator!", ephemeral=True)
            return
        c = self.config
        # Value should be one of 0, 1, or 2 corresponding to the different sensitivities
        if interaction.data['values'][0] in ['0', '1', '2']:
            c.sensitivity = int(interaction.data['values'][0])

        # Invalidate cache
        self.client.invalidate_config_cache(interaction.guild_id)

        # Update initial message with new option
        e, v = _config_gui_internal(c, self.client, interaction)
        await interaction.response.edit_message(embed=e, view=v)
        v.message = interaction.message

        # Set the config in the DB
        set_config(interaction.guild_id, c)


# Allows for enabling/disabling the reporting feature in a server
class ReportingButton(discord.ui.Button):
    def __init__(self, config: Config, client: MyClient, interaction: discord.Interaction):
        self.client = client
        self.interaction = interaction
        self.config = config
        super().__init__(label=("Disable" if config.reporting else "Enable") + " Reporting")

    async def callback(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            # User is not administrator, notify them and return
            await interaction.response.send_message("You are not an administrator!", ephemeral=True)
            return
        c = self.config

        # Toggle reporting in config
        if c.reporting:
            c.reporting = False
        else:
            c.reporting = True

        # Update initial message
        e, v = _config_gui_internal(c, self.client, interaction)
        self.client.invalidate_config_cache(interaction.guild_id)
        await interaction.response.edit_message(embed=e, view=v)
        v.message = interaction.message

        # Set the config in the DB
        set_config(interaction.guild_id, c)

# Helper method to make a dropdown option for a channel
def channel_option(c: discord.TextChannel, emoji="#️⃣", default=False):
    return discord.SelectOption(label=c.name, value=str(c.id), emoji=emoji, default=default)

# Allows for selecting the feedback channel in the configuration
class ChannelDropdown(discord.ui.Select):
    def __init__(self, config: Config, interaction: discord.Interaction):
        # Max options in Discord dropdown are 25, so keep running var of amount of items
        c = 1
        # Add "none" option to the dropdown
        options = [discord.SelectOption(label="None", value="None", emoji="❌")]

        # Add selected channel to the top of the list
        current_channel = interaction.guild.get_channel(config.feedback_channel)
        if current_channel is not None:
            options.append(channel_option(current_channel, default=True, emoji="✨"))
            c += 1

        # Add current channel to top of the dropdown
        if isinstance(interaction.channel, discord.TextChannel) and current_channel != interaction.channel:
            options.append(channel_option(interaction.channel, emoji="🔶"))
            c += 1

        # Iterate over the channels in the guild
        #
        # NOTE: while loop could be used, but we need "i" var anyways,
        # so it just brings down line count by 1 to use for loop
        for i in range(25):
            if c < 25:
                try:
                    if interaction.channel == interaction.guild.channels[i] or current_channel == \
                            interaction.guild.channels[i]:
                        continue
                    if isinstance(interaction.guild.channels[i], discord.TextChannel):
                        options.append(channel_option(interaction.guild.channels[i]))
                        c += 1
                except IndexError:
                    break

        self.config = config
        self.interaction = interaction

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Feedback Channel', min_values=1, max_values=1, options=options,
                         custom_id="channel_select")

    # Called when the user clicks on a dropdown item
    async def callback(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You are not an administrator!", ephemeral=True)
            return
        c = self.config
        if interaction.data['values'][0] == "None":
            # User selected "none" option, reset the feedback channel
            c.feedback_channel = None

            interaction.client.invalidate_config_cache(interaction.guild_id)
            e, v = _config_gui_internal(c, interaction.client, interaction)
            v.message = interaction.message
            await interaction.response.edit_message(embed=e, view=v)

            set_config(interaction.guild_id, c)
            return
        try:
            # Try to set the channel
            channel = int(interaction.data['values'][0])
            c.feedback_channel = channel

            interaction.client.invalidate_config_cache(interaction.guild_id)
            e, v = _config_gui_internal(c, interaction.client, interaction)
            v.message = interaction.message
            await interaction.response.edit_message(embed=e, view=v)

            set_config(interaction.guild_id, c)
        except ValueError:
            pass

# Main view for configuration
class ConfigView(discord.ui.View):
    def __init__(self, config: Config, client: MyClient, interaction: discord.Interaction):
        super().__init__()

        self.timeout = 60
        self.interaction = interaction

        # Add all of the menu items
        self.add_item(SensitivityDropdown(config, client, interaction))
        self.add_item(ChannelDropdown(config, interaction))
        self.add_item(ReportingButton(config, client, interaction))

    async def on_timeout(self) -> None:
        # Step 2
        for item in self.children:
            item.disabled = True

        # Step 3
        try:
            await self.message.edit(view=self)
        except discord.errors.NotFound:
            pass

# Create embed and view from config
def _config_gui_internal(config: Config, client: MyClient, interaction: discord.Interaction):
    embed = discord.Embed(title="Toxicity Bot Settings", color=discord.Color.brand_green(),
                          description="You can access these settings by using the `/toxicity config` command")
    embed.add_field(name="Sensitivity", value="This option defines how sensitive the bot's model should be when "
                                              "filtering bad language.")
    embed.add_field(name="Reporting", value="This option defines if server members should be able to report "
                                            "messages in this server.")
    view = ConfigView(config, client, interaction)

    return embed, view

# Create embed and view from guild_id
def create_config_gui(id: int, client: MyClient, interaction: discord.Interaction):
    return _config_gui_internal(get_config(id), client, interaction)
