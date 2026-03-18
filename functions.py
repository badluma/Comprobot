import os
import re
from typing import Dict, List, cast

import appdirs
import discord
import ollama

from bot import client
from data import ai, history


def para(count=1):
    for i in range(count):
        print()


def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


async def direct_msg(message, author_message):
    user = await client.fetch_user(author_message.author.id)
    dm_channel = user.dm_channel
    if dm_channel is None:
        dm_channel = await user.create_dm()
    try:
        await dm_channel.send(message)
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
    messages: List[Dict[str, str]] = cast(List[Dict[str, str]], history["messages"])
    user_id = client.user.id if client.user else ""

    messages.append(
        {
            "role": "user",
            "content": message.content.replace(f"<@{user_id}>", ""),
        }
    )

    response = ollama.chat(model=cast(str, ai["model"]), messages=messages)

    content: str = response.message.content or ""

    messages.append({"role": "assistant", "content": content})

    max_total = 1 + cast(int, ai["max_messages_context"])
    while len(messages) > max_total:
        messages.pop(1)

    if ai["remove_emojis"]:
        content = demoji(content)
    if ai["lower_response"]:
        content = content.lower()

    return content


def create(path, content, is_dir=False):
    base_dir = appdirs.user_data_dir(appname="Comprobot", appauthor=False)

    if not os.path.isdir(base_dir):
        os.makedirs(base_dir, exist_ok=True)

    final_path = os.path.join(base_dir, path)

    if is_dir:
        os.makedirs(final_path, exist_ok=True)
    else:
        os.makedirs(os.path.dirname(final_path), exist_ok=True)
        if not os.path.isfile(final_path):
            with open(final_path, "w") as file:
                file.write(content)
