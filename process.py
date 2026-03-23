from typing import Any, cast

import api
import commands
import money_system
from bot import client
from data import active, config, error_messages, keywords, success_messages


async def process(message) -> str | None | Any:

    if message.content.startswith(cast(str, config["prefix"])):
        command_parts = message.content[1:].strip().split()

        command = command_parts[0]
        args = command_parts[1:]

        # print(command_parts)
        # print(command)
        # print(args)

        if command in keywords["quote"] and active["quote"]:
            return api.quote()
        elif command in keywords["joke"] and active["joke"]:
            return api.joke()
        elif command in keywords["dadjoke"] and active["dadjoke"]:
            return api.dadjoke()
        elif command in keywords["meme"] and active["meme"]:
            return api.meme()
        elif command in keywords["waifu"] and active["waifu"]:
            if args:
                if args[0] in keywords["nsfw"] and active["nsfw"]:
                    return api.waifu(True)
                else:
                    return api.waifu(False)
            else:
                return api.waifu(False)
        elif command in keywords["image"] and active["image"]:
            if args[0] in keywords["duck"] and active["duck"]:
                return api.duck()
            elif args[0] in keywords["dog"] and active["dog"]:
                return api.dog()
            elif args[0] in keywords["cat"] and active["cat"]:
                return api.cat()
            elif not args:
                return error_messages["missing_argument"]
            else:
                return error_messages["unknown_argument"]
        elif command in keywords["chuck_norris"] and active["chuck_norris"]:
            return api.chuck()
        elif command in keywords["fact"] and active["fact"]:
            return api.fact()
        elif command in keywords["bible"] and active["bible"]:
            return api.bible()

        elif command in keywords["truth"] and active["truth"]:
            return api.tord(
                "https://api.truthordarebot.xyz/v1/truth", args[0] if args else None
            )
        elif command in keywords["dare"] and active["dare"]:
            return api.tord(
                "https://api.truthordarebot.xyz/api/dare", args[0] if args else None
            )
        elif command in keywords["wyr"] and active["wyr"]:
            return api.tord(
                "https://api.truthordarebot.xyz/api/wyr", args[0] if args else None
            )
        elif command in keywords["never_have_i_ever"] and active["never_have_i_ever"]:
            return api.tord(
                "https://api.truthordarebot.xyz/api/nhie", args[9] if args else None
            )
        elif command in keywords["paranoia"] and active["paranoia"]:
            return api.tord(
                "https://api.truthordarebot.xyz/api/paranoia", args[0] if args else None
            )

        elif command in keywords["qr_code"] and active["qr_code"]:
            return commands.qr(args[0])

        elif command in keywords["currency"] and active["currency"]:
            if not len(args) >= 3:
                return error_messages["missing_argument"]
            return api.currency(args[0], args[1], args[2])

        elif command in keywords["check_balance"]:
            if args:
                return money_system.check_balance(args[0])
            else:
                return error_messages["missing_argument"]
        elif command in keywords["add_money"] and (
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
        elif command in keywords["remove_money"] and (
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

        elif command in keywords["settings"] and (
            message.author.guild_permissions.administrator
            or message.author.name in config["bot_admins"]
        ):
            if not args:
                return error_messages["missing_argument"]

            if args[0] in keywords["profile_picture"]:
                if not message.attachments:
                    return error_messages["no_attachments"]
                if client is None or client.user is None:
                    return error_messages["bot_unavailable"]
                new_pfp = message.attachments[0]
                await new_pfp.save("Cache/pfp.png")
                with open("Cache/pfp.png", "rb") as image_file:
                    image_data = image_file.read()
                await client.user.edit(avatar=image_data)
                return success_messages["profile_picture_applied"]

            elif args[0] in keywords["banner"]:
                if not message.attachments:
                    return error_messages["no_attachments"]
                if client is None or client.user is None:
                    return error_messages["bot_unavailable"]
                new_banner = message.attachments[0]
                await new_banner.save("Cache/banner.png")
                with open("Cache/banner.png", "rb") as image_file:
                    image_data = image_file.read()
                await client.user.edit(banner=image_data)
                return success_messages["banner_applied"]

            elif args[0] in keywords["change_name"]:
                if len(args) < 2:
                    return error_messages["missing_argument"]
                if client is None or client.user is None:
                    return error_messages["bot_unavailable"]
                await client.user.edit(username=args[1])
                return success_messages["nickname_applied"]

            elif args[0] in keywords["keywords"]:
                if len(args) < 2:
                    return error_messages["missing_argument"]
                keywords[args[1]] = args[2:]

        elif command == "purge" and active["purge"]:
            if message.author.guild_permissions.administrator:
                await message.channel.purge()
                return "All messages deleted."

        else:
            return error_messages["unknown_command"]

    return None
