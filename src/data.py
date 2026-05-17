import os
from collections.abc import Mapping
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import appdirs
import tomlkit
import tomlkit.exceptions

from . import templates

DATA_DIR: str = os.environ.get("COMPROBOT_DATA_DIR") or appdirs.user_data_dir(
    "Comprobot"
)

Migration = Union[Tuple[str, str], Callable]

RENAME_COMMANDS: List[Migration] = [("commands", "general")]


def get_data_path(filename: str) -> str:
    return os.path.join(DATA_DIR, filename)


def _write(path: str, data) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        tomlkit.dump(data, f)


def _apply_migrations(data, migrations: List[Migration]) -> bool:
    changed = False
    for migration in migrations:
        if callable(migration):
            changed |= bool(migration(data))
        else:
            old_key, new_key = migration
            if old_key in data:
                if new_key not in data:
                    data[new_key] = data[old_key]
                del data[old_key]
                changed = True
    return changed


def _merge_defaults(data, defaults) -> bool:
    changed = False
    for key, value in defaults.items():
        if key not in data:
            data[key] = value
            changed = True
        elif isinstance(value, Mapping) and isinstance(data.get(key), Mapping):
            changed |= _merge_defaults(data[key], value)
    return changed


def _reorder(data, defaults) -> bool:
    in_data = set(data.keys())
    target = [k for k in defaults if k in in_data] + [
        k for k in in_data if k not in defaults
    ]

    if list(data.keys()) == target:
        changed = False
        for key in defaults:
            if isinstance(defaults[key], Mapping) and isinstance(
                data.get(key), Mapping
            ):
                changed |= _reorder(data[key], defaults[key])
        return changed

    snapshot = {k: data[k] for k in in_data}
    for key in list(in_data):
        del data[key]
    for key in target:
        data[key] = snapshot[key]

    for key in defaults:
        if isinstance(defaults[key], Mapping) and isinstance(data.get(key), Mapping):
            _reorder(data[key], defaults[key])

    return True


def _prune(data, defaults) -> bool:
    changed = False
    for key in [k for k in data if k not in defaults]:
        del data[key]
        changed = True
    for key, value in defaults.items():
        if isinstance(value, Mapping) and isinstance(data.get(key), Mapping):
            changed |= _prune(data[key], value)
    return changed


def load_or_create(
    path: str,
    template_content: str,
    migrations: Optional[List[Migration]] = None,
    prune_obsolete: bool = True,
) -> dict:
    defaults = tomlkit.loads(template_content)

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = tomlkit.loads(f.read())
    except FileNotFoundError:
        _write(path, defaults)
        return defaults
    except tomlkit.exceptions.TOMLKitError:
        backup = path + ".bak"
        os.replace(path, backup)
        print(
            f"[Comprobot] Corrupt TOML at {path!r} — backed up to {backup!r}, resetting to defaults."
        )
        _write(path, defaults)
        return defaults

    changed = _apply_migrations(data, migrations or [])
    changed |= _merge_defaults(data, defaults)
    if prune_obsolete:
        changed |= _prune(data, defaults)
    changed |= _reorder(data, defaults)

    if changed:
        _write(path, data)

    return data


def save_toml(data, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        tomlkit.dump(data, f)


error_messages: Dict[str, str] = load_or_create(
    get_data_path("error-messages.toml"), templates.error_messages
)
config: Dict[str, Any] = load_or_create(get_data_path("config.toml"), templates.config)
keywords: Dict[str, Dict[str, List[str]]] = load_or_create(
    get_data_path("keywords.toml"), templates.keywords, migrations=RENAME_COMMANDS
)
ai: Dict[str, Any] = load_or_create(get_data_path("ai.toml"), templates.ai)
system_prompt_text: str = str(ai["system_prompt"])
money: Dict[str, Dict[str, int]] = load_or_create(
    get_data_path("money.toml"), "[members]\n", prune_obsolete=False
)
active: Dict[str, Any] = load_or_create(get_data_path("active.toml"), templates.active)
output: Dict[str, Dict[str, List[str]]] = load_or_create(
    get_data_path("output.toml"), templates.output, migrations=RENAME_COMMANDS
)
moderation: Dict[Any, Any] = load_or_create(
    get_data_path("moderation.toml"), templates.moderation
)
descriptions: Dict[str, Dict[str, str]] = load_or_create(
    get_data_path("descriptions.toml"),
    templates.descriptions,
    migrations=RENAME_COMMANDS,
)

env_path = get_data_path(".env")
if not os.path.isfile(env_path):
    os.makedirs(os.path.dirname(env_path), exist_ok=True)
    with open(env_path, "w", encoding="utf-8") as f:
        f.write(templates.env)
