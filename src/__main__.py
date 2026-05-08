import argparse

import dotenv

from .data import active, ai, get_data_path, save_toml
from .main import main
from .onboarding import onboarding


def cli_main():
    parser = argparse.ArgumentParser(
        prog="comprobot",
        description="A self-hostable open-source Discord bot built for maximum customization.",
    )
    subparsers = parser.add_subparsers(dest="command", metavar="")
    subparsers.add_parser("onboard", help="Set up Comprobot for the first time.")
    subparsers.add_parser("start", help="Start the bot.")
    test_parser = subparsers.add_parser("test", help="Process a message through the bot's command processor.")
    test_parser.add_argument("message", help="The message to process (e.g. '!calculate 2+2')")

    args = parser.parse_args()

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

            save_toml(ai, get_data_path("ai.toml"))
            save_toml(active, get_data_path("active.toml"))

            main()

        case "test":
            from .testing import run_test
            run_test(args.message)

        case _:
            print(parser.format_help())


if __name__ == "__main__":
    cli_main()
