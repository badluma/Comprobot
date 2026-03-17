import os
import re
import appdirs
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

    # Keep system prompt (index 0) + max 5 messages (total 6)
    max_total = 1 + ai["max_messages_context"]
    while len(history["messages"]) > max_total:
        history["messages"].pop(1)  # Remove from index 1 to keep system prompt

    if ai["remove_emojis"]:
        response = demoji(response.message.content)
    if ai["lower_response"]:
        response = response.lower()

    return response


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
