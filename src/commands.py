import asyncio

from random import choice

from .data import active, config, error_messages, keywords, output, descriptions


def qr(link):
    url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={link}"
    return choice(output["general"]["qr_code"]).replace(r"{{URL}}", url)


def calculate(calculation):
    try:
        result = eval(calculation)
        response = choice(output["general"]["calculate"]).replace(
            r"{{RESULT}}", str(result)
        )
    except ZeroDivisionError:
        response = error_messages["calculate"]
    except Exception:
        response = error_messages["calculate"]
    return response


def help(category=None):
    if not category:
        message = "# Categories"

        for category in list(keywords.keys()):
            message += f"\n**{category.title()}**\n!help {category}\n-# \u200b"
        return message
    else:
        if category.lower() not in list(keywords.keys()):
            return error_messages["unknown_category"]
        message = f"## {category.title()}\n"
        for command in list(keywords[category.lower()].keys()):
            if active.get(category.lower(), {}).get(command, True):
                message += f"\n**{config['prefix']}{keywords[category.lower()][command][0]}** - {descriptions[category.lower()][command]}"
                if len(keywords[category.lower()][command]) > 1:
                    message += f"\n-# Aliases: {', '.join(config['prefix'] + alias for alias in keywords[category.lower()][command][1:])}"
                message += "\n-# \u200b"
        return message


def ascii():
    if not config["ascii_art"]:
        return error_messages["no_ascii_art"]
    return choice(output["general"]["ascii_art"]).replace(
        r"{{ASCII_ART}}", choice(config["ascii_art"])
    )

async def reminder(args, ctx):
    if len(args) < 2:
        return error_messages["missing_argument"]

    time_arg = args[0]
    message = " ".join(args[1:])

    match time_arg[-1]:
        case "s":
            time = int(time_arg[:-1])
        case "m":
            time = int(time_arg[:-1]) * 60
        case "h":
            time = int(time_arg[:-1]) * 3600
        case _:
            return error_messages["unknown_unit"]

    await ctx.send(f"Reminder '{message}' sending in {time_arg}.")

    await asyncio.sleep(time)
    await ctx.author.send(message)
