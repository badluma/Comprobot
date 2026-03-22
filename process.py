from typing import Any, cast

import api
import commands
import money_system
from bot import client
from data import config, error_messages, keywords, success_messages


async def process(message) -> str | None | Any:

    if message.content.startswith(cast(str, config["prefix"])):
        command_parts = message.content[1:].strip().split()

        command = command_parts[0]
        args = command_parts[1:]

        # print(command_parts)
        # print(command)
        # print(args)

        if command in keywords["quote"]:
            return api.quote()
        elif command in keywords["joke"]:
            return api.joke()
        elif command in keywords["meme"]:
            return api.meme()
        elif command in keywords["image"]:
            if args[0] in keywords["duck"]:
                return api.duck()
            elif args[0] in keywords["dog"]:
                return api.dog()
            elif args[0] in keywords["cat"]:
                return api.cat()
            elif not args:
                return error_messages["no_argument_given"]
            else:
                return error_messages["unknown_argument"]
        elif command in keywords["chuck_norris"]:
            return api.chuck()
        elif command in keywords["fact"]:
            return api.fact()
        elif command in keywords["bible"]:
            return api.bible()

        elif command in keywords["truth"]:
            return api.tord(
                "https://api.truthordarebot.xyz/v1/truth", args[0] if args else None
            )
        elif command in keywords["dare"]:
            return api.tord(
                "https://api.truthordarebot.xyz/api/dare", args[0] if args else None
            )
        elif command in keywords["wyr"]:
            return api.tord(
                "https://api.truthordarebot.xyz/api/wyr", args[0] if args else None
            )
        elif command in keywords["never_have_i_ever"]:
            return api.tord(
                "https://api.truthordarebot.xyz/api/nhie", args[9] if args else None
            )
        elif command in keywords["paranoia"]:
            return api.tord(
                "https://api.truthordarebot.xyz/api/paranoia", args[0] if args else None
            )

        elif command in keywords["qr_code"]:
            return commands.qr(args[0])

        elif command in keywords["check_balance"]:
            if args:
                return money_system.check_balance(args[0])
            else:
                return error_messages["no_argument_given"]
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
                return error_messages["no_argument_given"]

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
                    return error_messages["no_argument_given"]
                if client is None or client.user is None:
                    return error_messages["bot_unavailable"]
                await client.user.edit(username=args[1])
                return success_messages["nickname_applied"]

            elif args[0] in keywords["keywords"]:
                if len(args) < 2:
                    return error_messages["no_argument_given"]
                keywords[args[1]] = args[2:]

        elif command == "purge":
            if message.author.guild_permissions.administrator:
                await message.channel.purge()
                return "All messages deleted."

        else:
            return error_messages["unknown_command"]

    return None
