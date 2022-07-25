from dotenv import load_dotenv
import discord
import os
import pandas as pd

load_dotenv()

class MyClient(discord.Client):
    async def on_ready(self):
        data = pd.DataFrame()
        if (input("Should scrape Discord? (y/n) ") == "y"):
            print('Logged on as {0}!'.format(self.user))
            contents = []
            for channel in client.get_all_channels():
                if isinstance(channel, discord.TextChannel):
                    async for msg in channel.history(limit=30):
                        contents.append(msg.content)
            data['text'] = contents
            data['class'] = 0
            print('Saving Discord data...')
        else:
            data = pd.read_csv('../data/discord-data.csv')
            print('Loaded data from file...')

        data.to_csv('../data/discord-data.csv', index=False)



client = MyClient()
client.run(os.environ.get("BOT_TOKEN"))
