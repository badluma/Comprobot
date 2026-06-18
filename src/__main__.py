import argparse
import os
import tomlkit
from os import path

from importlib.metadata import metadata as pkg_metadata



def main():
    parser = argparse.ArgumentParser(
        prog="comprobot",
        description="A self-hostable open-source Discord bot built for maximum customization.",
    )
    subparsers = parser.add_subparsers(dest="command", metavar="")
    parser.add_argument("-v", "--version", action="store_true", help="Show the current version number.")
    parser.add_argument("--dashboard-version", action="store_true", help="Show the compatible dashboard version (used by the installer).")
    subparsers.add_parser("reset", help="Reset the bot's configuration.")
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
    dashboard_parser = subparsers.add_parser("dashboard", help="Start the web dashboard.")
    dashboard_parser.add_argument(
        "-w", "--watch", action="store_true", help="Run dashboard in the foreground."
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

    if getattr(args, "dashboard_version", False):
        from .dashboard import DASHBOARD_VERSION

        print(DASHBOARD_VERSION)
        return

    if getattr(args, "version", False):
        meta = pkg_metadata("comprobot")
        version = meta["Version"]
        name = meta["Name"]
        full = f"\n█▀▀▀▀▀█\n█ █ █ █  {name.title()} v{version}\n█▄▄▄▄▄█"
        print(full)
        return

    match args.command:
        case "start":
            from .start import start

            start(daemon=getattr(args, "daemon", False))

        case "dashboard":
            from .dashboard import launch

            launch(foreground=getattr(args, "watch", False))

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

        case "reset":
            from .data import ai, config, error_messages, keywords, moderation, active, descriptions, output, get_data_path

            with open(get_data_path("ai.toml"), "w") as f:
                tomlkit.dump(ai, f)
            with open(get_data_path("active.toml"), "w") as f:
                tomlkit.dump(active, f)
            with open(get_data_path("config.toml"), "w") as f:
                tomlkit.dump(config, f)
            with open(get_data_path("error_messages.toml"), "w") as f:
                tomlkit.dump(error_messages, f)
            with open(get_data_path("keywords.toml"), "w") as f:
                tomlkit.dump(keywords, f)
            with open(get_data_path("moderation.toml"), "w") as f:
                tomlkit.dump(moderation, f)
            with open(get_data_path("descriptions.toml"), "w") as f:
                tomlkit.dump(descriptions, f)
            with open(get_data_path("output.toml"), "w") as f:
                tomlkit.dump(output, f)


        case _:
            print(parser.format_help())


if __name__ == "__main__":
    main()
