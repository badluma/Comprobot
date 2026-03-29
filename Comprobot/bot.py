import discord
import os
import dotenv
import appdirs

dotenv.load_dotenv(
    dotenv.find_dotenv(
        os.path.join(
            appdirs.user_data_dir(appname="Comprobot", appauthor=False), ".env"
        )
    )
)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
