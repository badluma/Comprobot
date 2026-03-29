from typing import Any, Dict, List

import tomlkit

import templates


def _get_data_path(filename):
    import os

    import appdirs

    base_dir = appdirs.user_data_dir(appname="Comprobot", appauthor=False)
    return os.path.join(base_dir, filename)


def _ensure_file(path, content):
    import os

    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.isfile(path):
        with open(path, "w") as f:
            f.write(content)


def _merge_defaults(data, defaults):
    for key, value in defaults.items():
        if key not in data:
            data[key] = value
        elif isinstance(value, dict) and isinstance(data.get(key), dict):
            _merge_defaults(data[key], value)


def _load_or_create(path, template_content):
    try:
        with open(path, "rb") as f:
            data = tomlkit.load(f)
    except FileNotFoundError:
        _ensure_file(path, template_content)
        with open(path, "rb") as f:
            data = tomlkit.load(f)

    defaults = tomlkit.loads(template_content)
    _merge_defaults(data, defaults)

    if data != defaults:
        with open(path, "w") as f:
            tomlkit.dump(data, f)

    return data


ai_str = templates.ai

error_messages: Dict[str, str] = _load_or_create(
    _get_data_path("error-messages.toml"), templates.error_messages
)
success_messages: Dict[str, str] = _load_or_create(
    _get_data_path("success_messages.toml"), templates.success_messages
)
config: Dict[str, Any] = _load_or_create(
    _get_data_path("config.toml"), templates.config
)
keywords: Dict[str, Dict[str, List[str]]] = _load_or_create(
    _get_data_path("keywords.toml"), templates.keywords
)
ai: Dict[str, Any] = _load_or_create(_get_data_path("ai.toml"), ai_str)
system_prompt_text = ai["system_prompt"]
money: Dict[str, Dict[str, int]] = _load_or_create(
    _get_data_path("money.toml"), r"""balances = {}"""
)
active: Dict[str, bool] = _load_or_create(
    _get_data_path("active.toml"), templates.active
)

_ensure_file(_get_data_path(".env"), templates.env_template)


def save_toml(data, path):
    with open(path, "w") as f:
        tomlkit.dump(data, f)
