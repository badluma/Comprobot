import asyncio
import os
import re
import subprocess
from typing import Any, Dict, List, cast

import discord
import httpx
import ollama

from .bot import client
from .data import DATA_DIR, ai

context_memory: Dict[int, List[Dict[str, Any]]] = {}


def para(count=1):
    for i in range(count):
        print()


def clear():
    if os.name == "nt":
        subprocess.call("cls")
    else:
        subprocess.call("clear")


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


async def get_referenced_message(message):
    if not message.reference:
        return None

    if isinstance(message.reference.resolved, discord.Message):
        return message.reference.resolved

    try:
        return await message.channel.fetch_message(message.reference.message_id)
    except discord.NotFound:
        return None


async def chat(message):
    user_id = client.user.id if client.user else ""
    channel_id = message.channel.id

    if channel_id not in context_memory:
        context_memory[channel_id] = []

    messages = context_memory[channel_id]

    referenced_message = await get_referenced_message(message)

    # Construct user content based on templates
    attachment_url = ""
    if message.attachments and ai["include_attachment"]:
        attachment_url = message.attachments[0].url
    elif referenced_message and ai["include_attachment"]:
        if referenced_message.attachments:
            attachment_url = referenced_message.attachments[0].url

    user_prompt_content = (
        ai["user_prompt_structure"]
        .replace("{{PROMPT}}", ai["user_prompt"])
        .replace(
            "{{REPLY_PROMPT}}",
            ai["user_reply_prompt"]
            if ai["include_reply"] and referenced_message
            else "",
        )
        .replace(
            "{{ATTACHMENT_PROMPT}}",
            ai["user_attachement_prompt"].replace("{{FILE}}", attachment_url)
            if attachment_url
            else "",
        )
        .replace(
            "{{USERNAME}}",
            message.author.display_name if ai["include_username"] else "",
        )
        .replace("{{MESSAGE}}", message.content.replace(f"<@{user_id}>", ""))
        .replace(
            "{{REPLY}}",
            referenced_message.content
            if referenced_message and ai["include_reply"]
            else "",
        )
    )

    # Add user message to history
    messages.append({"role": "user", "content": user_prompt_content})

    # Limit context
    max_total = cast(int, ai["max_messages_context"])
    while len(messages) > max_total:
        messages.pop(0)

    provider = ai["provider"].lower()
    content = ""

    if provider == "ollama":
        formatted_messages = [
            {"role": "system", "content": ai["system_prompt_text"]}
        ] + messages
        response = ollama.chat(
            model=cast(str, ai["model"]), messages=formatted_messages
        )
        content = response.message.content or ""
    elif provider == "gemini":
        formatted_messages = []
        for m in messages:
            formatted_messages.append(
                {
                    "role": "user" if m["role"] == "user" else "model",
                    "parts": [{"text": m["content"]}],
                }
            )
        body: Dict[str, Any] = {"contents": formatted_messages}
        if ai["system_prompt_text"]:
            body["systemInstruction"] = {"parts": [{"text": ai["system_prompt_text"]}]}

        async with httpx.AsyncClient() as http:
            resp = None
            for attempt in range(4):
                resp = await http.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/{ai['model']}:generateContent",
                    params={"key": os.getenv("GEMINI")},
                    json=body,
                    timeout=60,
                )
                if resp.status_code != 429:
                    break
                data = resp.json()
                retry_delay = None
                is_daily_quota = False
                for detail in data.get("error", {}).get("details", []):
                    if "retryDelay" in detail:
                        retry_delay = detail["retryDelay"]
                    if "violations" in detail:
                        for v in detail["violations"]:
                            if "PerDay" in v.get("quotaId", ""):
                                is_daily_quota = True
                if is_daily_quota or attempt == 3:
                    resp.raise_for_status()
                match = re.search(r"(\d+(?:\.\d+)?)", retry_delay or "")
                wait = float(match.group(1)) if match else min(30 * (2**attempt), 120)
                await asyncio.sleep(wait)
            if resp is None:
                raise RuntimeError("Gemini request never sent")
            if resp.status_code == 404:
                print(
                    f"Model '{ai['model']}' not found. Check ai.toml for valid model name."
                )
            resp.raise_for_status()
            content = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
    elif provider == "groq":
        formatted_messages = [
            {"role": "system", "content": ai["system_prompt_text"]}
        ] + messages
        async with httpx.AsyncClient() as http:
            resp = await http.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {os.getenv('GROQ')}"},
                json={"model": ai["model"], "messages": formatted_messages},
                timeout=60,
            )
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"] or ""
    else:
        raise ValueError(f"Unknown provider: {ai['provider']}")

    # Add assistant message to history
    messages.append({"role": "assistant", "content": content})

    # Prune again after adding assistant message
    while len(messages) > max_total:
        messages.pop(0)

    if ai["remove_emojis"]:
        content = demoji(content)
    if ai["lower_response"]:
        content = content.lower()

    content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
    return content


def create(path, content, is_dir=False):
    base_dir = DATA_DIR

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
