import argparse

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
        case "start" | None:
            main()
        case "onboard":
            settings = onboarding()
        case _:
            quit()
