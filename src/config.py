import sys
import os

import appdirs
import tomlkit

import InquirerPy.utils
from InquirerPy.base.control import Choice
from InquirerPy.prompts import confirm, input, secret
from InquirerPy.prompts import list as inquirer_list

style = InquirerPy.utils.InquirerPyStyle(
    {
        "instruction": "#aaaaaa italic",
        "questionmark": "#5865F2 bold",
        "answermark": "#5865F2",
        "answer": "#5865F2",
        "question": "#ffffff",
    }
)


def make_pretty(string):
    return (
        string.replace(".toml", "")
        .replace("_", " ")
        .replace("-", " ")
        .title()
        .replace("Ai", "AI")
        .replace("Api", "API")
    )


def pick_file():
    data_dir = appdirs.user_data_dir("Comprobot", appauthor=False)

    files = {}

    for file in os.listdir(data_dir):
        if not file.endswith(".toml"):
            continue
        files[file] = {}
        files[file]["path"] = os.path.join(data_dir, file)
        files[file]["display"] = make_pretty(file)

    if not files:
        print("No configuration files found.")
        sys.exit(1)

    env_path = os.path.join(appdirs.user_data_dir("Comprobot", appauthor=False), ".env")

    file_to_edit = inquirer_list.ListPrompt(
        message="Which file do you want to edit?",
        choices=[
            Choice(value=files[file]["path"], name=files[file]["display"])
            for file in files
        ]
        + ([Choice(value=env_path, name="Secrets")] if os.path.exists(env_path) else [])
        + [Choice(value="exit", name="Exit")],
        style=style,
        amark="!",
        vi_mode=True,
        show_cursor=False,
    ).execute()

    if file_to_edit == "exit":
        sys.exit(0)

    if file_to_edit == env_path:
        from dotenv import dotenv_values

        content = {k: v or "" for k, v in dotenv_values(file_to_edit).items()}
        return (file_to_edit, content)

    with open(file_to_edit, "r") as f:
        content = tomlkit.load(f)

    return (file_to_edit, content)


def pick_key(content, is_secret=False):

    print()

    key = inquirer_list.ListPrompt(
        message="Which key do you want to edit?",
        choices=[
            Choice(value=key, name=make_pretty(key)) for key in list(content.keys())
        ]
        + [Choice(value="exit", name="Exit")],
        style=style,
        amark="!",
        show_cursor=False,
        vi_mode=True,
    ).execute()

    if key == "exit":
        sys.exit(0)

    match content[key]:
        case dict():
            pick_key(content[key], is_secret=is_secret)

        case bool():
            print()
            value = confirm.ConfirmPrompt(
                message=f"Do you want to set '{make_pretty(key)}' to True or False?",
                instruction=f"(y/n) (Current: {content[key]})",
                style=style,
                amark="!",
                vi_mode=True,
            ).execute()
            content[key] = value

        case str():
            print()
            if is_secret:
                value = secret.SecretPrompt(
                    message=f"New value for '{make_pretty(key)}'?",
                    style=style,
                    amark="!",
                    vi_mode=True,
                ).execute()
            else:
                value = input.InputPrompt(
                    message=f"What value do you want to assign to '{make_pretty(key)}'?",
                    instruction=f"(Current: {content[key]})",
                    style=style,
                    amark="!",
                    vi_mode=True,
                ).execute()
            content[key] = value

        case int():
            print()
            if is_secret:
                value = secret.SecretPrompt(
                    message=f"New value for '{make_pretty(key)}'?",
                    style=style,
                    amark="!",
                    vi_mode=True,
                ).execute()
            else:
                value = input.InputPrompt(
                    message=f"What number do you want to assign to '{make_pretty(key)}'?",
                    instruction=f"(Current: {content[key]})",
                    style=style,
                    amark="!",
                    vi_mode=True,
                ).execute()

            if not int(value):
                content[key] = 0
                return

            content[key] = int(value)

        case list():
            print()
            value = (
                input.InputPrompt(
                    message=f"What values do you want to assign to '{make_pretty(key)}'?",
                    instruction=f"(separate by commas) (Current: {', '.join(content[key]) if content[key] else 'None'})",
                    style=style,
                    amark="!",
                    vi_mode=True,
                )
                .execute()
                .split(",")
            )
            content[key] = [item.strip() for item in value if item.strip()]


def configure(args):

    if not args:
        print()
        try:
            file_to_edit, content = pick_file()
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

        is_secret = file_to_edit.endswith(".env")

        while True:
            try:
                pick_key(content, is_secret=is_secret)
            except KeyboardInterrupt:
                sys.exit(0)
            except Exception as e:
                print(f"Error: {e}")
                continue

            if is_secret:
                from dotenv import set_key as dotenv_set_key

                for k, v in content.items():
                    dotenv_set_key(
                        dotenv_path=file_to_edit, key_to_set=k, value_to_set=v
                    )
            else:
                with open(file_to_edit, "w") as f:
                    tomlkit.dump(content, f)
    else:
        if len(args) < 3:
            print("Usage: config <file> <key> <value(s)>")
            sys.exit(1)

        file_name, key, *values = args

        data_dir = appdirs.user_data_dir("Comprobot", appauthor=False)

        if file_name == "secrets":
            from dotenv import set_key as dotenv_set_key

            env_path = os.path.join(data_dir, ".env")
            if not os.path.exists(env_path):
                print(".env file not found.")
                sys.exit(1)
            if not values:
                print("Usage: config secrets <key> <value>")
                sys.exit(1)
            dotenv_set_key(dotenv_path=env_path, key_to_set=key, value_to_set=values[0])
            return

        file_path = os.path.join(data_dir, f"{file_name}.toml")

        if not os.path.exists(file_path):
            print(f"File '{file_name}.toml' not found.")
            sys.exit(1)

        with open(file_path, "r") as f:
            content = tomlkit.load(f)

        if key not in content:
            print(f"Key '{key}' not found in {file_name}.toml.")
            sys.exit(1)

        current = content[key]

        match current:
            case bool():
                v = values[0].lower()
                if v not in ("true", "false"):
                    print(
                        f"Invalid value '{values[0]}' for bool. Use 'true' or 'false'."
                    )
                    sys.exit(1)
                content[key] = v == "true"
            case list():
                content[key] = values
            case str():
                content[key] = values[0]
            case int():
                try:
                    content[key] = int(values[0])
                except ValueError:
                    print(f"Invalid value '{values[0]}' for int key.")
                    sys.exit(1)

        with open(file_path, "w") as f:
            tomlkit.dump(content, f)
