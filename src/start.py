import os
import platform
import sys
from os import getenv as os_getenv

import dotenv

from .bot import client
from .data import DATA_DIR, get_data_path
from .functions import para
from .process import Comprobot

dotenv.load_dotenv(dotenv.find_dotenv(get_data_path(".env")))

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
async def on_ready():
    user_name = client.user.name if client.user else "Unknown"
    print(f"Logged in as {user_name}")
    para()


def _daemonize():
    if os.fork() != 0:
        os._exit(0)
    os.setsid()
    if os.fork() != 0:
        os._exit(0)
    devnull = os.open(os.devnull, os.O_RDONLY)
    os.dup2(devnull, 0)
    os.close(devnull)


def start(daemon=False, data_dir=DATA_DIR):
    if daemon:
        _daemonize()
    print(f"Configuration directory: {data_dir}")
    token = os_getenv("BOT_TOKEN")
    if token:
        from .dashboard import launch as launch_dashboard

        launch_dashboard(foreground=False)
        client.run(token)
    else:
        print("Error: BOT_TOKEN not found in environment variables")
