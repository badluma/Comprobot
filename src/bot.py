import os

import appdirs
import discord
import dotenv
from discord.ext import commands

dotenv.load_dotenv(
    dotenv.find_dotenv(
        os.path.join(
            appdirs.user_data_dir(appname="Comprobot", appauthor=False), ".env"
        )
    )
)

intents = discord.Intents.default()
intents.message_content = True

from .data import config  # noqa: E402

bot = commands.Bot(
    command_prefix=lambda b, m: config["prefix"],
    intents=intents,
    help_command=None,
)
client = bot
