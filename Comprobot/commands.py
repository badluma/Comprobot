import random

from .data import config, error_messages


def qr(link):
    return f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={link}"


def calculate(calculation):
    try:
        result = eval(calculation)
        response = f"Result: {result}"
    except Exception as e:
        response = f"{error_messages['calculate']} (error {str(e)})"
    return response


def ascii():
    return random.choice(config["ascii_art"])
