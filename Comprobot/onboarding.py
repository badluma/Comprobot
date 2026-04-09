import os

import InquirerPy.utils
import tomlkit
from InquirerPy.base.control import Choice
from InquirerPy.prompts import checkbox, confirm, input, secret
from InquirerPy.prompts import list as inquirer_list

ACCENT = "\033[0;36m"
GRAY = "\u001b[0;37m"
RESET = "\033[0m"

style = InquirerPy.utils.InquirerPyStyle({"questionmark": "white"})


def onboarding():
    from . import templates

    active_data = tomlkit.loads(templates.active)
    all_commands = list(active_data.keys())
    active_choices = [Choice(value, enabled=True) for value in all_commands]

    print(f"\n{ACCENT}Welcome to Comprobot{RESET}")
    print("Thank you so much for downloading this bot!")
    print("I am going to guide you through the process of setting it up.")
    print(f"- First, go to {ACCENT}discord.com/developers/applications{RESET}.")
    print("- Create a new application.")
    print(
        f"- Under the {ACCENT}Bot{RESET} section, you can customize the bot's name, avatar and banner."
    )
    print(f"- Next, head to the {ACCENT}OAuth2{RESET} section.")
    print(
        f"- Under {ACCENT}OAuth2 URL Generator{RESET}, select only the {ACCENT}bot{RESET} option."
    )
    print(
        f"- Then, scroll down to {ACCENT}Bot Permissions{RESET} and select {ACCENT}Administrator{RESET}."
    )
    print(
        f"- Copy the link and open it in a new tab. Select your server, then click {ACCENT}Continue{RESET} and {ACCENT}Authorize{RESET}"
    )
    print(
        f"- Back on the {ACCENT}Application dashboard{RESET}, head back to the {ACCENT}Bot{RESET} section."
    )
    print(
        f"- Click on {ACCENT}Reset Token{RESET} and then on {ACCENT}Yes, do it!{RESET}."
    )
    print("- Copy the new token and paste it here.")
    print()

    try:
        # 1. Bot Token
        token = secret.SecretPrompt(
            message="Your bot token:",
            style=style,
            vi_mode=True,
        ).execute()

        print()

        # 2. Commands to activate
        commands_activated = checkbox.CheckboxPrompt(
            message="Select commands to activate:",
            instruction="Press Space to deselect and press Enter to continue.",
            choices=active_choices,
            style=style,
            transformer=lambda result: (
                f"{len(result)} commands selected" if result else "No commands selected"
            ),
            show_cursor=False,
        ).execute()

        print()

        # 3. Activate AI features
        ai_activated = confirm.ConfirmPrompt(
            message="Do you want to activate AI features?", style=style, default=True
        ).execute()
        if ai_activated:
            print()

            # 3.1. Select provider
            provider = inquirer_list.ListPrompt(
                message="Select a provider:",
                choices=[
                    Choice(value="groq", name="Groq (recommended)"),
                    Choice(value="gemini", name="Gemini"),
                    Choice(value="ollama", name="Ollama (local)"),
                ],
                default="groq",
                style=style,
                show_cursor=False,
            ).execute()

            match provider:
                case "groq":
                    print()
                    print(
                        f"To get your forever-free Groq API key, head to {ACCENT}console.groq.com/keys{RESET}."
                    )
                    print(
                        "Create an account and then create a new API key without an expiration date."
                    )
                    print("Then copy the API key and paste it here.")
                case "gemini":
                    print()
                    pass
                case "ollama":
                    pass
                case _:
                    ai_activated = False
                    provider = None
                    api_key = None

            if provider in ["groq", "gemini"]:
                print()

                # 3.2. Get API key
                api_key = secret.SecretPrompt(
                    message="Your API key:",
                    style=style,
                    vi_mode=True,
                ).execute()
            else:
                api_key = None

            model = input.InputPrompt(
                message="Enter the model you want to use:",
                style=style,
                vi_mode=True,
            )

        else:
            model = None
            provider = None
            api_key = None

        print()

    except KeyboardInterrupt:
        quit()

    env_path = os.path.join(
        appdirs.user_data_dir(appname="Comprobot", appauthor=False), ".env"
    )
    with open(env_path, "w") as f:
        f.write(f"BOT_TOKEN={token}\n")
        if api_key:
            if provider == "groq":
                f.write(f"GROQ={api_key}\n")
            elif provider == "gemini":
                f.write(f"GEMINI={api_key}\n")

    result = {
        "token": token,
        "commands_activated": commands_activated,
        "ai_activated": ai_activated,
        "provider": provider,
        "api_key": api_key,
        "model": model,
        "file_path": file_path,
    }

    print(result)
    return result
