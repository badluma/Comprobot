from data.data import *


def add_money(username, amount):
    money["members"][username] = money["members"].get(username, 0) + amount
    save_toml(money, "data/.do_not_touch/money.toml")
    return (
        f"{money['members'][username]}{config['money_symbol']} added to to {username}"
    )


def remove_money(username, amount):
    current = money["members"].get(username, 0)
    if current < amount:
        money["members"][username] = 0
        save_toml(money, "data/.do_not_touch/money.toml")
        return f"{username} doesn't have enough money. They now have 0{config['money_symbol']}."
    else:
        money["members"][username] -= amount
        save_toml(money, "data/.do_not_touch/money.toml")
        return f"{amount} subtracted from {username}. They now have {money['members'][username]}{config['money_symbol']}."


def check_balance(username):
    try:
        return f"{money['members'][username]}{config['money_symbol']}"
    except KeyError:
        money["members"][username] = 0
        save_toml(money, "data/.do_not_touch/money.toml")
        return f"0{config['money_symbol']}"
