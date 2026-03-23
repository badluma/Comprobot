import platform
import sys
from os import getenv as os_getenv
from os import path as os_path
from typing import cast

import appdirs
import discord
import dotenv

import process
from data import ai, config
from functions import chat, client, para

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

    print(
        "\033[90m"
        + f"[{message.channel}] "
        + "\033[36m"
        + f"{message.author.name}: "
        + "\033[0m"
        + message.content
    )

    global response

    if message.author == client.user:
        return
    response = None

    if message.content.startswith(cast(str, config["command_prefix"])):
        async with message.channel.typing():
            response = await process.command(message)
    if message.content.startswith(cast(str, config["settings_prefix"])):
        async with message.channel.typing():
            response = await process.settings(message)

    is_reply_to_bot = False
    user_id = client.user.id if client.user else None
    if message.reference and message.reference.message_id and user_id:
        try:
            ref_msg = await message.channel.fetch_message(message.reference.message_id)
            is_reply_to_bot = ref_msg.author.id == user_id
        except discord.NotFound:
            pass

    if (f"<@{user_id}>" in message.content or is_reply_to_bot) and ai.get(
        "activate_ai", False
    ):
        async with message.channel.typing():
            response = chat(message)

    if response:
        async with message.channel.typing():
            content = str(response)
            for chunk in [content[i : i + 2000] for i in range(0, len(content), 2000)]:
                await message.channel.send(chunk)


@client.event
async def on_ready():
    print(
        f"Configuration directory: {appdirs.user_data_dir(appname='Comprobot', appauthor=False)}"
    )
    user_name = client.user.name if client.user else "Unknown"
    print(f"Logged in as {user_name}")
    para()


if __name__ == "__main__":
    token = os_getenv("BOT_TOKEN")
    if token:
        client.run(token)
