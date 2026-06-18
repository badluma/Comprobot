import discord
import dotenv
from discord.ext import commands

from .data import config, get_data_path

dotenv.load_dotenv(dotenv.find_dotenv(get_data_path(".env")))

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(
    command_prefix=lambda b, m: config["prefix"],
    intents=intents,
    help_command=None,
)


@client.event
async def on_message(message):
    # Intentionally empty — Comprobot Cog handles on_message and
    # calls process_commands explicitly. This overrides the Bot's
    # default on_message (which also calls process_commands) so
    # commands don't fire twice.
    pass
