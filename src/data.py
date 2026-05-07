import os
from typing import Any, Dict, List

import appdirs
import tomlkit

from . import templates


def get_data_path(filename):

    base_dir = appdirs.user_data_dir(appname="Comprobot", appauthor=False)
    return os.path.join(base_dir, filename)


def ensure_file(path, content):

    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.isfile(path):
        with open(path, "w") as f:
            f.write(content)


def merge_defaults(data, defaults):
    for key, value in defaults.items():
        if key not in data:
            data[key] = value
        elif isinstance(value, dict) and isinstance(data.get(key), dict):
            merge_defaults(data[key], value)


def load_or_create(path, template_content):
    try:
        with open(path, "rb") as f:
            data = tomlkit.load(f)
    except FileNotFoundError:
        ensure_file(path, template_content)
        with open(path, "rb") as f:
            data = tomlkit.load(f)

    defaults = tomlkit.loads(template_content)
    merge_defaults(data, defaults)

    if data != defaults:
        with open(path, "w") as f:
            tomlkit.dump(data, f)

    return data


error_messages: Dict[str, str] = load_or_create(
    get_data_path("error-messages.toml"), templates.error_messages
)
config: Dict[str, Any] = load_or_create(get_data_path("config.toml"), templates.config)
keywords: Dict[str, Dict[str, List[str]]] = load_or_create(
    get_data_path("keywords.toml"), templates.keywords
)
ai: Dict[str, Any] = load_or_create(get_data_path("ai.toml"), templates.ai)
system_prompt_text = ai["system_prompt"]
money: Dict[str, Dict[str, int]] = load_or_create(
    get_data_path("money.toml"), r"""members = {}"""
)
active: Dict[str, bool] = load_or_create(get_data_path("active.toml"), templates.active)
output: Dict[str, Dict[str, List[str]]] = load_or_create(
    get_data_path("output.toml"), templates.output
)
moderation: Dict[Any, Any] = load_or_create(
    get_data_path("moderation.toml"), templates.moderation
)

ensure_file(get_data_path(".env"), templates.env)


def save_toml(data, path):
    with open(path, "w") as f:
        tomlkit.dump(data, f)
