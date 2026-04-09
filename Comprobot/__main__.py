import argparse

import dotenv

from .data import active, ai, config
from .main import main
from .onboarding import onboarding

parser = argparse.ArgumentParser(
    prog="comprobot",
    description="A self-hostable open-source Discord bot built for maximum customization.",
)
subparsers = parser.add_subparsers(dest="command", metavar="")
subparsers.add_parser("onboard", help="Set up Comprobot for the first time.")
subparsers.add_parser("start", help="Start the bot.")
# subparsers.add_parser("config", help="View or edit the bot's configuration.") TODO: implement config command
# subparsers.add_parser("reset", help="Reset the bot's data and configuration.") TODO: implement reset command

args = parser.parse_args()

settings: dict = {}

if __name__ == "__main__":
    match args.command:
        case "start":
            main()
        case "onboard":
            settings = onboarding()

            dotenv.set_key(
                dotenv_path=".env",
                key_to_set="BOT_TOKEN",
                value_to_set=str(settings["token"]),
            )

            for key in active:
                if key in settings["commands_activated"]:
                    active[key] = True
                else:
                    active[key] = False

            ai["activated"] = settings["ai_activated"]

            ai["provider"] = settings["provider"]

            if settings["provider"] == "groq":
                dotenv.set_key(
                    dotenv_path=".env",
                    key_to_set="GROQ",
                    value_to_set=settings["api_key"],
                )
                dotenv.set_key(dotenv_path=".env", key_to_set="GEMINI", value_to_set="")

            elif settings["provider"] == "gemini":
                dotenv.set_key(
                    dotenv_path=".env",
                    key_to_set="GEMINI",
                    value_to_set=settings["api_key"],
                )
                dotenv.set_key(dotenv_path=".env", key_to_set="GROQ", value_to_set="")

            else:
                dotenv.set_key(dotenv_path=".env", key_to_set="GROQ", value_to_set="")
                dotenv.set_key(dotenv_path=".env", key_to_set="GEMINI", value_to_set="")

            if settings["model"]:
                ai["model"] = settings["model"]
            else:
                ai["model"] = ""

        case _:
            print(parser.format_help())
