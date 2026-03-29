import os
from typing import Any

from appdirs import user_cache_dir, user_data_dir

from . import api
from . import commands
from . import data
from . import money_system
from .bot import client
from .data import active, config, error_messages, keywords, success_messages


async def command(ctx) -> str | None | Any:

    command_parts = ctx.content[len(config["command_prefix"]) :].strip().split()

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

    elif command in keywords["commands"]["ascii_art"]:
        return commands.ascii()

    elif command in keywords["commands"]["currency"] and active["currency"]:
        if not len(args) >= 3:
            return error_messages["missing_argument"]
        return api.currency(args[0], args[1], args[2])

    elif command in keywords["money"]["check_balance"]:
        if args:
            return money_system.check_balance(args[0])
        else:
            return error_messages["missing_argument"]
    elif command in keywords["money"]["add_money"] and (
        ctx.author.guild_permissions.administrator or config["bot_admins"]
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
        ctx.author.guild_permissions.administrator or config["bot_admins"]
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
        if ctx.author.guild_permissions.administrator:
            await ctx.channel.purge()
            return "All messages deleted."

    else:
        return None


async def settings(ctx):

    command_parts = ctx.content[len(config["settings_prefix"]) :].strip().split()

    command = command_parts[0]
    args = command_parts[1:]

    cache_dir = user_cache_dir("Comprobot", appauthor=False)
    os.makedirs(cache_dir, exist_ok=True)

    if command in keywords["settings"]["profile_picture"]:
        if not ctx.attachments:
            return error_messages["no_attachments"]
        if client is None or client.user is None:
            return error_messages["bot_unavailable"]
        new_pfp = ctx.attachments[0]
        await new_pfp.save(f"{cache_dir}/pfp.png")
        with open(f"{cache_dir}/pfp.png", "rb") as image_file:
            image_data = image_file.read()
        await client.user.edit(avatar=image_data)
        return success_messages["profile_picture_applied"]

    elif command in keywords["settings"]["banner"]:
        if not ctx.attachments:
            return error_messages["no_attachments"]
        if client is None or client.user is None:
            return error_messages["bot_unavailable"]
        new_banner = ctx.attachments[0]
        await new_banner.save(f"{cache_dir}/banner.png")
        with open(f"{cache_dir}/banner.png", "rb") as image_file:
            image_data = image_file.read()
        await client.user.edit(banner=image_data)
        return success_messages["banner_applied"]

    elif command in keywords["settings"]["change_name"]:
        if len(args) < 2:
            return error_messages["missing_argument"]
        if client is None or client.user is None:
            return error_messages["bot_unavailable"]
        await client.user.edit(username=args[1])
        return success_messages["nickname_applied"]

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

        return success_messages["keywords_applied"]

    else:
        return error_messages["unknown_command"]


async def games(ctx):
    pass
