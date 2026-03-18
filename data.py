from typing import Any, Dict, List, cast

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


def _load_or_create(path, template_content):
    try:
        with open(path, "rb") as f:
            return tomlkit.load(f)
    except FileNotFoundError:
        _ensure_file(path, template_content)
        with open(path, "rb") as f:
            return tomlkit.load(f)


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
keywords: Dict[str, List[str]] = _load_or_create(
    _get_data_path("keywords.toml"), templates.keywords
)
ai: Dict[str, Any] = _load_or_create(_get_data_path("ai.toml"), ai_str)
money: Dict[str, Dict[str, int]] = _load_or_create(
    _get_data_path("money.toml"), r"""balances = {}"""
)

ai_parsed = tomlkit.loads(ai_str)
system_prompt_text = cast(str, ai_parsed["system_prompt"])

conversation_history_template = templates.conversation_history.replace(
    "You are a helpful assistant.", system_prompt_text
)
history: Dict[str, List[Dict[str, str]]] = _load_or_create(
    _get_data_path("conversation_history.toml"), conversation_history_template
)

history_messages = cast(List[Dict[str, str]], history["messages"])
history_messages[0]["content"] = system_prompt_text


def save_toml(data, path):
    with open(path, "w") as f:
        tomlkit.dump(data, f)
