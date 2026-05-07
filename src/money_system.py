from random import choice
from . import data
import tomlkit
import tomlkit.exceptions


def add_money(username, amount):
    data.money["members"][username] = data.money["members"].get(username, 0) + amount
    data.save_toml(data.money, data.get_data_path("money.toml"))
    balance = data.money["members"][username]
    return (
        choice(data.output["money"]["add_money"])
        .replace("{{AMOUNT}}", str(amount))
        .replace("{{USERNAME}}", username)
        .replace("{{BALANCE}}", str(balance))
        .replace("{{MONEY_SYMBOL}}", data.config["money_symbol"])
    )


def remove_money(username, amount):
    current = data.money["members"].get(username, 0)
    if current < amount:
        data.money["members"][username] = 0
        data.save_toml(data.money, data.get_data_path("money.toml"))
        return (
            choice(data.output["money"]["insufficient_funds"])
            .replace("{{USERNAME}}", username)
            .replace("{{BALANCE}}", str(0))
            .replace("{{MONEY_SYMBOL}}", data.config["money_symbol"])
        )
    else:
        data.money["members"][username] -= amount
        data.save_toml(data.money, data.get_data_path("money.toml"))
        balance = data.money["members"][username]
        return (
            choice(data.output["money"]["remove_money"])
            .replace("{{AMOUNT}}", str(amount))
            .replace("{{USERNAME}}", username)
            .replace("{{BALANCE}}", str(balance))
            .replace("{{MONEY_SYMBOL}}", data.config["money_symbol"])
        )


def check_balance(username):
    try:
        balance = data.money["members"][username]
    except (KeyError, tomlkit.exceptions.NonExistentKey):
        data.money["members"][username] = 0
        data.save_toml(data.money, data.get_data_path("money.toml"))
        balance = 0
    return (
        choice(data.output["money"]["check_balance"])
        .replace("{{USERNAME}}", username)
        .replace("{{BALANCE}}", str(balance))
        .replace("{{MONEY_SYMBOL}}", data.config["money_symbol"])
    )
