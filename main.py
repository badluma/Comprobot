import os

import commands
import moderation
from functions import *
import functions
import process
import dotenv

import discord
import ollama

from bot import client

dotenv.load_dotenv()

from data.data import *

response = None


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

    if message.content.startswith(config["prefix"]):
        async with message.channel.typing():
            response = await process.process(message)

    is_reply_to_bot = False
    if message.reference and message.reference.message_id:
        try:
            ref_msg = await message.channel.fetch_message(message.reference.message_id)
            is_reply_to_bot = ref_msg.author.id == client.user.id
        except discord.NotFound:
            pass

    if f"<@{client.user.id}>" in message.content or is_reply_to_bot:
        async with message.channel.typing():
            response = chat(message)

    if response:
        async with message.channel.typing():
            content = (
                str(response.message.content)
                if hasattr(response, "message")
                else str(response)
            )
            for chunk in [content[i : i + 2000] for i in range(0, len(content), 2000)]:
                await message.channel.send(chunk)


@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")
    para()


if __name__ == "__main__":
    client.run(os.getenv("BOT_TOKEN"))
