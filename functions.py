import os
import re
import discord
import ollama
from bot import client
from data.data import *


def para(count=1):
    for i in range(count):
        print()


def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


# Discord-related


async def direct_msg(message, author_message):
    user = await client.fetch_user(author_message.author.id)
    if user.dm_channel is None:
        await user.create_dm()
    try:
        await user.dm_channel.send(message)
    except (discord.Forbidden, discord.HTTPException):
        print(f"Couldn't DM {author_message.author.name}.")


def demoji(text):
    emoji_pattern = re.compile(
        "["
        "\U0001f600-\U0001f64f"  # emoticons
        "\U0001f300-\U0001f5ff"  # symbols & pictographs
        "\U0001f680-\U0001f6ff"  # transport & map symbols
        "\U0001f1e0-\U0001f1ff"  # flags (iOS)
        "\U00002702-\U000027b0"
        "\U000024c2-\U0001f251"
        "\U0001f926-\U0001f937"
        "\U00010000-\U0010ffff"
        "\u200d"
        "\u2640-\u2642"
        "\u2600-\u2b55"
        "\u23cf"
        "\u23e9"
        "\u231a"
        "\ufe0f"  # variation selectors
        "\u3030"
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub("", text)


def chat(message):
    # Add user message
    history["messages"].append(
        {
            "role": "user",
            "content": message.content.replace(f"<@{client.user.id}>", ""),
        }
    )

    # Get response
    response = ollama.chat(model=ai["model"], messages=history["messages"])

    # Add assistant response to history
    history["messages"].append(
        {"role": "assistant", "content": response.message.content}
    )

    if len(history["messages"]) > ai["max_messages_context"]:
        history["messages"].pop(0)

    if ai["remove_emojis"]:
        response = demoji(response.message.content)
    if ai["lower_response"]:
        response = response.lower()

    return response
