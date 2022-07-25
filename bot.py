from dotenv import load_dotenv
from toxicity import predict
import discord
import os
from toxicity.clean import clean_text

load_dotenv()


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if not message.author.permissions_in(message.channel).manage_messages or os.environ.get("IS_TEST").lower() == "true":
            if predict([clean_text(message.content)]):
                await message.delete()


client = MyClient()
client.run(os.environ.get("BOT_TOKEN"))
