import tomlkit

with open("data/error-messages.toml", "rb") as f:
    error_messages = tomlkit.load(f)
with open("data/success_messages.toml", "rb") as f:
    success_messages = tomlkit.load(f)
with open("data/config.toml", "rb") as f:
    config = tomlkit.load(f)
with open("data/keywords.toml", "rb") as f:
    keywords = tomlkit.load(f)
with open("data/ai.toml", "rb") as f:
    ai = tomlkit.load(f)
with open("data/.do_not_touch/money.toml", "rb") as f:
    money = tomlkit.load(f)
with open("data/.do_not_touch/conversation_history.toml", "rb") as f:
    history = tomlkit.load(f)

history["messages"][0]["content"] = ai["system_prompt"]


def save_toml(data, path):
    with open(path, "w") as f:
        tomlkit.dump(data, f)
