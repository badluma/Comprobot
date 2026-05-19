import os
from typing import Any, Dict, List

import appdirs
import json
import tomlkit
import tomlkit.exceptions

from . import templates

DATA_DIR: str = os.environ.get("COMPROBOT_DATA_DIR") or appdirs.user_data_dir(
    "Comprobot"
)

ORDER = ["general", "games", "settings"]



def get_data_path(filename: str) -> str:
    return os.path.join(DATA_DIR, filename)

def _load_or_create(filename: str, template: dict) -> dict:
    file_path = get_data_path(filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    if not os.path.isfile(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            tomlkit.dump(template, f)

    with open(file_path, "r", encoding="utf-8") as f:
        return tomlkit.load(f)

def save_toml(data: dict, file_path: str) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        tomlkit.dump(data, f)


def _cleanup(file_path: str, template: dict, order=ORDER) -> dict:

    result = _load_or_create(file_path, template)
    template = json.loads(json.dumps(template))

    for category in list(result.keys()):
        if category not in template:
            del result[category]
            continue
        if not isinstance(template[category], dict):
            continue
        for key in list(result[category].keys()):
            if template[category] and key not in template[category]:
                del result[category][key]

    for category, cat_template in template.items():
        if category not in result:
            result[category] = cat_template if not isinstance(cat_template, dict) else {}
        if isinstance(cat_template, dict):
            for key, value in cat_template.items():
                if key not in result[category]:
                    result[category][key] = value

    result = {k: result[k] for k in order if k in result} | {k: v for k, v in result.items() if k not in order}

    with open(file_path, "w", encoding="utf-8") as f:
        tomlkit.dump(result, f)

    return result

def _load_data(file_path: str, template: dict, order: list = ORDER) -> dict:
    return _cleanup(get_data_path(file_path), template, order)


error_messages: Dict[str, str] = _load_data("error_messages.toml", templates.error_messages)
config: Dict[str, Any] = _load_data("config.toml", templates.config)
keywords: Dict[str, Dict[str, List[str]]] = _load_data("keywords.toml", templates.keywords)
ai: Dict[str, Any] = _load_data("ai.toml", templates.ai)
money: Dict[str, Dict[str, int]] = _load_data(".money.toml", {"members": {}})
active: Dict[str, Any] = _load_data("active.toml", templates.active)
output: Dict[str, Dict[str, List[str]]] = _load_data("output.toml", templates.output)
moderation: Dict[Any, Any] = _load_data("moderation.toml", templates.moderation)
descriptions: Dict[str, Dict[str, str]] = _load_data("descriptions.toml", templates.descriptions)

env_path = get_data_path(".env")
if not os.path.isfile(env_path):
    os.makedirs(os.path.dirname(env_path), exist_ok=True)
    with open(env_path, "w", encoding="utf-8") as f:
        f.write(templates.env)
