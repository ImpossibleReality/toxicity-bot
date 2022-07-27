import discord
from db import Config, get_config, set_config


class SensitivityDropdown(discord.ui.Select):
    def __init__(self, config: Config):
        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label='Loose', description='Flags only severe hate speech and profanity', emoji='🟢',
                                 default=config.sensitivity == 0, value="0"),
            discord.SelectOption(label='Moderate', description='Flags moderate hate speech and profanity', emoji='🟠',
                                 default=config.sensitivity == 1, value="1"),
            discord.SelectOption(label='Strict', description='Flags mild profanity and all hate speech', emoji='🔴',
                                 default=config.sensitivity == 2, value="2"),
        ]

        self.config = config

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Sensitivity', min_values=1, max_values=1, options=options, custom_id="config_select")

    async def callback(self, interaction: discord.Interaction):
        c = self.config
        if interaction.data['values'][0] in ['0', '1', '2']:
            c.sensitivity = int(interaction.data['values'][0])

        e, v = _config_gui_internal(c)
        await interaction.response.edit_message(embed=e, view=v)
        set_config(interaction.guild_id, c)



class FeedbackButton(discord.ui.Button):
    def __init__(self, config: Config):
        self.config = config
        super().__init__(label=("Disable" if config.feedback else "Enable") + " Feedback")

    async def callback(self, interaction: discord.Interaction):
        c = self.config

        if c.feedback:
            c.feedback = False
        else:
            c.feedback = True

        e, v = _config_gui_internal(c)
        await interaction.response.edit_message(embed=e, view=v)
        set_config(interaction.guild_id, c)


class ConfigView(discord.ui.View):
    def __init__(self, config: Config):
        super().__init__()

        self.add_item(SensitivityDropdown(config))
        self.add_item(FeedbackButton(config))


def _config_gui_internal(config: Config):
    embed = discord.Embed(title="Toxicity Bot Settings", color=discord.Color.brand_green(),
                          description="You can access these settings by using the `/toxicity config` command")
    embed.add_field(name="Sensitivity", value="This option defines how sensitive the bot's model should be when "
                                              "filtering bad language.")
    embed.add_field(name="Feedback", value="This option defines if server members should be able to give feedback on "
                                           "messages in this server.")
    view = ConfigView(config)

    return embed, view

def create_config_gui(id: int):
    return _config_gui_internal(get_config(id))

