import platform
import sys
from os import getenv as os_getenv
from os import path as os_path

import appdirs
import dotenv

from . import process
from .functions import client, para

dotenv.load_dotenv(
    dotenv.find_dotenv(
        os_path.join(
            appdirs.user_data_dir(appname="Comprobot", appauthor=False), ".env"
        )
    )
)


response = None
if sys.platform.startswith("win"):
    print("Running on Windows (cmd)")
elif platform.system() in ["Linux", "Darwin"]:
    pass
else:
    print("Unknown OS")


@client.event
async def on_message(message):
    await process.process(message)


@client.event
async def on_ready():
    user_name = client.user.name if client.user else "Unknown"
    print(f"Logged in as {user_name}")
    para()


def main():
    print(
        f"Configuration directory: {appdirs.user_data_dir(appname='Comprobot', appauthor=False)}"
    )
    token = os_getenv("BOT_TOKEN")
    if token:
        client.run(token)
    else:
        print("Error: BOT_TOKEN not found in environment variables")
