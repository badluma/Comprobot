import argparse
import os
from os import path


def main():
    parser = argparse.ArgumentParser(
        prog="comprobot",
        description="A self-hostable open-source Discord bot built for maximum customization.",
    )
    subparsers = parser.add_subparsers(dest="command", metavar="")
    start_parser = subparsers.add_parser("start", help="Start the bot.")
    start_parser.add_argument(
        "-d", "--daemon", action="store_true", help="Daemonize the process."
    )
    start_parser.add_argument(
        "-p",
        "--path",
        type=path.abspath,
        help="Choose a custom path for the bot's configuration.",
    )
    subparsers.add_parser("onboard", help="Set up Comprobot for the first time.")
    config_parser = subparsers.add_parser(
        "config", help="Configure the bot's settings."
    )
    config_parser.add_argument("config_args", nargs=argparse.REMAINDER)
    test_parser = subparsers.add_parser(
        "test", help="Process a message through the bot's command processor."
    )
    test_parser.add_argument(
        "message", help="The message to process (e.g. '!calculate 2+2')"
    )

    args = parser.parse_args()

    if getattr(args, "path", None):
        os.environ["COMPROBOT_DATA_DIR"] = args.path

    match args.command:
        case "start":
            from .start import start

            start(daemon=getattr(args, "daemon", False))

        case "onboard":
            from dotenv import set_key as dotenv_set_key
            from .data import active, ai, get_data_path, save_toml
            from .onboarding import onboarding
            from .start import start

            settings = onboarding()

            env_path = get_data_path(".env")

            dotenv_set_key(
                dotenv_path=env_path,
                key_to_set="BOT_TOKEN",
                value_to_set=str(settings["token"]),
            )

            for category in active:
                if isinstance(active[category], dict):
                    for key in active[category]:
                        active[category][key] = key in settings["commands_activated"]

            ai["activated"] = settings["ai_activated"]

            ai["provider"] = settings["provider"]

            if settings["provider"] == "groq":
                dotenv_set_key(
                    dotenv_path=env_path,
                    key_to_set="GROQ",
                    value_to_set=settings["api_key"],
                )
                dotenv_set_key(
                    dotenv_path=env_path, key_to_set="GEMINI", value_to_set=""
                )

            elif settings["provider"] == "gemini":
                dotenv_set_key(
                    dotenv_path=env_path,
                    key_to_set="GEMINI",
                    value_to_set=settings["api_key"],
                )
                dotenv_set_key(dotenv_path=env_path, key_to_set="GROQ", value_to_set="")

            else:
                dotenv_set_key(dotenv_path=env_path, key_to_set="GROQ", value_to_set="")
                dotenv_set_key(
                    dotenv_path=env_path, key_to_set="GEMINI", value_to_set=""
                )

            if settings["model"]:
                ai["model"] = settings["model"]
            else:
                ai["model"] = ""

            save_toml(ai, get_data_path("ai.toml"))
            save_toml(active, get_data_path("active.toml"))

            start()

        case "config":
            from .config import configure

            configure(args.config_args)

        case "test":
            from .testing import run_test

            run_test(args.message)

        case _:
            print(parser.format_help())


if __name__ == "__main__":
    main()
