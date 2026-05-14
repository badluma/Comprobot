import platform
import sys
from os import getenv as os_getenv
from os import path as os_path

import appdirs
import dotenv

from .bot import client
from .functions import para
from .process import Comprobot

dotenv.load_dotenv(
    dotenv.find_dotenv(
        os_path.join(
            appdirs.user_data_dir(appname="Comprobot", appauthor=False), ".env"
        )
    )
)

if sys.platform.startswith("win"):
    print("Running on Windows (cmd)")
elif platform.system() in ["Linux", "Darwin"]:
    pass
else:
    print("Unknown OS")


async def _setup_hook():
    await client.add_cog(Comprobot(client))


client.setup_hook = _setup_hook


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    ctx = await client.get_context(message)
    await client.invoke(ctx)


@client.event
async def on_ready():
    user_name = client.user.name if client.user else "Unknown"
    print(f"Logged in as {user_name}")
    para()


def start():
    print(
        f"Configuration directory: {appdirs.user_data_dir(appname='Comprobot', appauthor=False)}"
    )
    token = os_getenv("BOT_TOKEN")
    if token:
        client.run(token)
    else:
        print("Error: BOT_TOKEN not found in environment variables")
