from random import choice

from .data import config, error_messages, output


def qr(link):
    url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={link}"
    return choice(output["commands"]["qr_code"]).replace(r"{{URL}}", url)


def calculate(calculation):
    try:
        result = eval(calculation)
        response = choice(output["commands"]["calculate"]).replace(
            r"{{RESULT}}", str(result)
        )
    except ZeroDivisionError:
        response = error_messages["calculate"]
    except Exception:
        response = error_messages["calculate"]
    return response


def ascii():
    return choice(output["commands"]["ascii_art"]).replace(
        r"{{ASCII_ART}}", choice(config["ascii_art"])
    )
