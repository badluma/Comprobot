from . import data
from appdirs import user_data_dir


def add_money(username, amount):
    data.money["members"][username] = data.money["members"].get(username, 0) + amount
    data.save_toml(data.money, f"{user_data_dir('Comprobot')}/.dontchange/money.toml")
    return f"{data.money['members'][username]}{data.config['money_symbol']} added to to {username}"


def remove_money(username, amount):
    current = data.money["members"].get(username, 0)
    if current < amount:
        data.money["members"][username] = 0
        data.save_toml(
            data.money, f"{user_data_dir('Comprobot')}/.dontchange/money.toml"
        )
        return f"{username} doesn't have enough money. They now have 0{data.config['money_symbol']}."
    else:
        data.money["members"][username] -= amount
        data.save_toml(
            data.money, f"{user_data_dir('Comprobot')}/.dontchange/money.toml"
        )
        return f"{amount} subtracted from {username}. They now have {data.money['members'][username]}{data.config['money_symbol']}."


def check_balance(username):
    try:
        return f"{data.money['members'][username]}{data.config['money_symbol']}"
    except KeyError:
        data.money["members"][username] = 0
        data.save_toml(
            data.money, f"{user_data_dir('Comprobot')}/.dontchange/money.toml"
        )
        return f"0{data.config['money_symbol']}"
