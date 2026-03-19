import os
import re
from typing import Dict, List, cast
from google import genai
import groq

import appdirs
import discord
import ollama

from bot import client
from data import ai

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
    messages: List[Dict[str, str]] = cast(List[Dict[str, str]])
    user_id = client.user.id if client.user else ""

    if ai["provider"].lower() in ("ollama", "groq"):
        messages.append(
            {
                "role": "user",
                "content": message.content.replace(f"<@{user_id}>", ""),
            }
        )
    elif ai["provider"].lower() == "gemini":
        messages.append(
            {
                "role": "user",
                "parts": [{"text": message.content.replace(f"<@{user_id}>", "")}],
            }
        )
    else:
        raise ValueError(f"Unknown provider: {ai['provider']}")

    if ai["provider"].lower() == "ollama":
        response = ollama.chat(model=cast(str, ai["model"]), messages=messages)
        content: str = response.message.content or ""
    elif ai["provider"].lower() == "gemini":
        gemini_client = genai.Client(api_key=os.getenv("GEMINI"))
        system_instruction = None
        formatted_messages = []
        for m in messages:
            if m["role"] == "system":
                system_instruction = m["content"]
            else:
                formatted_messages.append(
                    {
                        "role": m["role"],
                        "parts": [
                            {"text": m["content"] if "content" in m else m["parts"][0]}
                        ],
                    }
                )
        config = None
        if system_instruction:
            config = genai.types.GenerateContentConfig(
                system_instruction=system_instruction
            )
        try:
            response = gemini_client.models.generate_content(
                model=ai["model"], contents=formatted_messages, config=config
            )
            content = response.text or ""
        except genai.errors.ClientError as e:
            if "NOT_FOUND" in str(e) or "404" in str(e):
                available = gemini_client.models.list()
                print(f"Available models: {[m.name for m in available]}")
            raise
    elif ai["provider"].lower() == "groq":
        groq_client = groq.Groq(api_key=os.getenv("GROQ"))
        formatted_messages = []
        for m in messages:
            if m["role"] == "system":
                formatted_messages.append(
                    {
                        "role": "system",
                        "content": m["content"],
                    }
                )
            else:
                formatted_messages.append(
                    {
                        "role": "user" if m["role"] == "user" else "assistant",
                        "content": m["content"],
                    }
                )
        response = groq_client.chat.completions.create(
            model=ai["model"], messages=formatted_messages
        )
        content = response.choices[0].message.content or ""
    else:
        raise ValueError(f"Unknown provider: {ai['provider']}")

    if ai["provider"].lower() == "groq":
        role = "assistant"
    elif ai["provider"].lower() == "ollama":
        role = "assistant"
    elif ai["provider"].lower() == "gemini":
        role = "model"
    else:
        raise ValueError(f"Unknown provider: {ai['provider']}")

    messages.append(
        {
            "role": role,
            "content": content,
        }
    )

    max_total = 1 + cast(int, ai["max_messages_context"])
    while len(messages) > max_total:
        messages.pop(1)

    if ai["remove_emojis"]:
        content = demoji(content)
    if ai["lower_response"]:
        content = content.lower()


    content = re.sub(r'<.*?>', '', content).strip()
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
