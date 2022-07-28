import discord

from bot import MyClient
from db import Config, get_config, set_config


class SensitivityDropdown(discord.ui.Select):
    def __init__(self, config: Config, client: MyClient):
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
        self.client = client

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Sensitivity', min_values=1, max_values=1, options=options,
                         custom_id="config_select")

    async def callback(self, interaction: discord.Interaction):
        c = self.config
        if interaction.data['values'][0] in ['0', '1', '2']:
            c.sensitivity = int(interaction.data['values'][0])
        self.client.invalidate_config_cache(interaction.guild_id)
        e, v = _config_gui_internal(c, self.client)
        await interaction.response.edit_message(embed=e, view=v)
        set_config(interaction.guild_id, c)


class FeedbackButton(discord.ui.Button):
    def __init__(self, config: Config, client: MyClient):
        self.client = client
        self.config = config
        super().__init__(label=("Disable" if config.reporting else "Enable") + " Reporting")

    async def callback(self, interaction: discord.Interaction):
        c = self.config

        if c.reporting:
            c.reporting = False
        else:
            c.reporting = True

        e, v = _config_gui_internal(c, self.client)
        self.client.invalidate_config_cache(interaction.guild_id)
        await interaction.response.edit_message(embed=e, view=v)
        set_config(interaction.guild_id, c)


class ConfigView(discord.ui.View):
    def __init__(self, config: Config, client: MyClient):
        super().__init__()

        self.timeout = 60

        self.add_item(SensitivityDropdown(config, client))
        self.add_item(FeedbackButton(config, client))

    async def on_timeout(self) -> None:
        # Step 2
        for item in self.children:
            item.disabled = True

        # Step 3
        await self.message.edit(view=self)


def _config_gui_internal(config: Config, client: MyClient):
    embed = discord.Embed(title="Toxicity Bot Settings", color=discord.Color.brand_green(),
                          description="You can access these settings by using the `/toxicity config` command")
    embed.add_field(name="Sensitivity", value="This option defines how sensitive the bot's model should be when "
                                              "filtering bad language.")
    embed.add_field(name="Reporting", value="This option defines if server members should be able to report "
                                            "messages in this server.")
    view = ConfigView(config, client)

    return embed, view


def create_config_gui(id: int, client: MyClient):
    return _config_gui_internal(get_config(id), client)
