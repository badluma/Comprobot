import os
from random import choice
from typing import Any, cast

import discord
from appdirs import user_cache_dir, user_data_dir

from . import api, commands, data, money_system
from .bot import client
from .data import active, ai, config, error_messages, keywords, output
from .functions import chat
from .moderation import check_message


async def command(message) -> str | None | Any:

    command_parts = message.content[len(config["command_prefix"]) :].strip().split()

    command = command_parts[0]
    args = command_parts[1:]

    if command in keywords["commands"]["quote"] and active["quote"]:
        return api.quote()
    elif command in keywords["commands"]["joke"] and active["joke"]:
        return api.joke()
    elif command in keywords["commands"]["meme"] and active["meme"]:
        return api.meme()
    elif command in keywords["commands"]["waifu"] and active["waifu"]:
        return api.waifu()
    elif command in keywords["commands"]["image"] and active["image"]:
        if args[0] in keywords["commands"]["duck"] and active["duck"]:
            return api.duck()
        elif args[0] in keywords["commands"]["dog"] and active["dog"]:
            return api.dog()
        elif args[0] in keywords["commands"]["cat"] and active["cat"]:
            return api.cat()
        elif not args:
            return error_messages["missing_argument"]
        else:
            return error_messages["unknown_argument"]
    elif command in keywords["commands"]["chuck_norris"] and active["chuck_norris"]:
        return api.chuck()
    elif command in keywords["commands"]["fact"] and active["fact"]:
        return api.fact()
    elif command in keywords["commands"]["bible"] and active["bible"]:
        if not args:
            return api.bible(True)
        if len(args) >= 3:
            return api.bible(False, args[0], args[1], args[2])
        return error_messages["passage_not_found"]
    elif command in keywords["commands"]["truth"] and active["truth"]:
        return api.tord(
            "https://api.truthordarebot.xyz/v1/truth", args[0] if args else None
        )
    elif command in keywords["commands"]["dare"] and active["dare"]:
        return api.tord(
            "https://api.truthordarebot.xyz/api/dare", args[0] if args else None
        )
    elif command in keywords["commands"]["wyr"] and active["wyr"]:
        return api.tord(
            "https://api.truthordarebot.xyz/api/wyr", args[0] if args else None
        )
    elif (
        command in keywords["commands"]["never_have_i_ever"]
        and active["never_have_i_ever"]
    ):
        return api.tord(
            "https://api.truthordarebot.xyz/api/nhie", args[0] if args else None
        )
    elif command in keywords["commands"]["paranoia"] and active["paranoia"]:
        return api.tord(
            "https://api.truthordarebot.xyz/api/paranoia", args[0] if args else None
        )

    elif command in keywords["commands"]["qr_code"] and active["qr_code"]:
        if args:
            return commands.qr(args[0])
        else:
            return error_messages["missing_argument"]

    elif command in keywords["commands"]["calculate"]:
        if args:
            return commands.calculate(args[0])
        else:
            return error_messages["missing_argument"]

    elif command in keywords["commands"]["bitcoin"] and active["bitcoin"]:
        return api.bitcoin(args[0] if args else "usd")

    elif command in keywords["commands"]["ascii_art"]:
        return commands.ascii()

    elif command in keywords["commands"]["currency"] and active["currency"]:
        if not len(args) >= 3:
            return error_messages["missing_argument"]
        return api.currency(args[1], args[2], args[0])

    elif command in keywords["money"]["check_balance"]:
        if args:
            return money_system.check_balance(args[0])
        else:
            return error_messages["missing_argument"]
    elif command in keywords["money"]["add_money"] and (
        message.author.guild_permissions.administrator or config["bot_admins"]
    ):
        if len(args) >= 2:
            try:
                amount = int(args[1])
                return money_system.add_money(args[0], amount)
            except ValueError:
                return f"Invalid amount: {args[1]}"
        else:
            return "No amount given."
    elif command in keywords["money"]["remove_money"] and (
        message.author.guild_permissions.administrator or config["bot_admins"]
    ):
        if len(args) >= 2:
            try:
                amount = int(args[1])
                return money_system.remove_money(args[0], amount)
            except ValueError:
                return f"Invalid amount: {args[1]}"
        else:
            return "No amount given."

    elif command == "purge" and active["purge"]:
        if message.author.guild_permissions.administrator:
            await message.channel.purge()
            return "All messages deleted."

    else:
        return None


async def settings(message):

    command_parts = message.content[len(config["settings_prefix"]) :].strip().split()

    command = command_parts[0]
    args = command_parts[1:]

    cache_dir = user_cache_dir("Comprobot", appauthor=False)
    os.makedirs(cache_dir, exist_ok=True)

    if command in keywords["settings"]["profile_picture"]:
        if not message.attachments:
            return error_messages["no_attachments"]
        if client is None or client.user is None:
            return error_messages["bot_unavailable"]
        new_pfp = message.attachments[0]
        await new_pfp.save(f"{cache_dir}/pfp.png")
        with open(f"{cache_dir}/pfp.png", "rb") as image_file:
            image_data = image_file.read()
        await client.user.edit(avatar=image_data)
        return choice(output["settings"]["profile_picture_applied"])

    elif command in keywords["settings"]["banner"]:
        if not message.attachments:
            return error_messages["no_attachments"]
        if client is None or client.user is None:
            return error_messages["bot_unavailable"]
        new_banner = message.attachments[0]
        await new_banner.save(f"{cache_dir}/banner.png")
        with open(f"{cache_dir}/banner.png", "rb") as image_file:
            image_data = image_file.read()
        await client.user.edit(banner=image_data)
        return choice(output["settings"]["banner_applied"])

    elif command in keywords["settings"]["change_name"]:
        if len(args) < 2:
            return error_messages["missing_argument"]
        if client is None or client.user is None:
            return error_messages["bot_unavailable"]
        await client.user.edit(username=args[1])
        return choice(output["settings"]["nickname_applied"]).replace(
            "{{NAME}}", " ".join(args[1:])
        )

    elif command in keywords["settings"]["change_keywords"]:
        if len(args) < 2:
            return error_messages["missing_argument"]

        target_category = None
        for category in keywords:
            if args[0] in keywords[category]:
                target_category = category
                break

        if target_category is None:
            return error_messages["unknown_argument"]

        keywords[target_category][args[0]] = args[1:]

        data.save_toml(keywords, f"{user_data_dir('Comprobot')}/keywords.toml")

        return (
            choice(output["settings"]["keywords_applied"])
            .replace("{{KEYWORDS}}", " ".join(args[1:]))
            .replace("{{COMMAND}}", args[0])
        )

    else:
        return error_messages["unknown_command"]


async def games(message):
    pass


async def process(message):
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

    await check_message(message)

    if message.content.startswith(cast(str, config["command_prefix"])):
        async with message.channel.typing():
            response = await command(message)
    elif message.content.startswith(cast(str, config["settings_prefix"])):
        async with message.channel.typing():
            response = await settings(message)

    is_reply_to_bot = False
    user_id = client.user.id if client.user else None
    if message.reference and message.reference.message_id and user_id:
        try:
            ref_msg = await message.channel.fetch_message(message.reference.message_id)
            is_reply_to_bot = ref_msg.author.id == user_id
        except discord.NotFound:
            pass

    if (
        f"<@{user_id}>" in message.content
        or (is_reply_to_bot if ai["answer_to_reply"] else False)
        and ai["activate_ai"]
    ):
        async with message.channel.typing():
            response = await chat(message)

    if response:
        async with message.channel.typing():
            content = str(response)
            for chunk in [content[i : i + 2000] for i in range(0, len(content), 2000)]:
                await message.channel.send(chunk)
