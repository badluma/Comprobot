import requests

from data import error_messages


def access_api(url, parameter, error_message, headers=None):
    if headers:
        raw = requests.get(url, headers=headers)
    else:
        raw = requests.get(url)
    if raw.status_code == 200:
        try:
            data = raw.json()
            response = data[parameter]
        except (requests.exceptions.JSONDecodeError, KeyError):
            response = str(f"{error_message}")
        except Exception as e:
            response = str(f"{error_message} (Error {str(e)})")
    else:
        response = str(f"{error_message} (HTTP {raw.status_code})")

    return response


# ---------- Commands ----------
def quote():
    quote_response = requests.get("https://zenquotes.io/api/random")
    try:
        data = quote_response.json()
        fetched_quote = data[0]["q"]
        author = data[0]["a"]
        response = f"""{fetched_quote}\n~{author}"""
    except (requests.exceptions.JSONDecodeError, KeyError, IndexError):
        response = error_messages["quote"]
    return response


def dadjoke():
    return access_api(
        "https://icanhazdadjoke.com/",
        "joke",
        error_messages["joke"],
        {"Accept": "application/json"},
    )


def meme():
    return access_api("https://meme-api.com/gimme", "url", error_messages["meme"])


def duck():
    return access_api("https://random-d.uk/api/random", "url", error_messages["duck"])


def dog():
    return access_api("https://random.dog/woojson", "url", error_messages["dog"])


def cat():
    raw = requests.get("https://api.thecatapi.com/v1/images/search")
    if raw.status_code == 200:
        try:
            data = raw.json()
            response = data[0]["url"]
        except (requests.exceptions.JSONDecodeError, KeyError, IndexError):
            response = error_messages["cat"]
    else:
        response = error_messages["cat"]
    return response


def chuck():
    return access_api(
        "https://api.chucknorris.io/jokes/random", "value", error_messages["chuck"]
    )


def fact():
    return access_api(
        "https://uselessfacts.jsph.pl/api/v2/facts/random",
        "text",
        error_messages["fact"],
    )


def bible():
    bible_response = requests.get("https://bible-api.com/data/web/random")
    if bible_response.status_code == 200:
        try:
            data = bible_response.json()
            if "random_verse" in data:
                verse = data["random_verse"]
                response = f"{verse['text']}{verse['book']} {verse['chapter']}, {verse['verse']}"
            else:
                response = error_messages["bible"]
        except (requests.exceptions.JSONDecodeError, KeyError):
            response = error_messages["bible"]
    else:
        response = f"{error_messages['bible']} (HTTP {bible_response.status_code})"
    return response


def calculate(calculation):
    try:
        result = eval(calculation)
        response = f"Result: {result}"
    except Exception as e:
        response = f"{error_messages['calculate']} (error {str(e)})"
    return response


def bitcoin(currency_parameter):
    currency = currency_parameter.lower() if len(str(currency_parameter)) > 1 else "usd"
    bitcoin_price = requests.get(
        f"https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies={currency}"
    )
    if bitcoin_price.status_code == 200:
        data = bitcoin_price.json()
        if "bitcoin" in data and currency in data["bitcoin"]:
            response = f"bitcoin is at {data['bitcoin'][currency]} {currency} rn"
        else:
            response = error_messages["currency"]
    else:
        response = error_messages["bitcoin"]
    return response


def tord(url, rating, max_retries=10):
    for _ in range(max_retries):
        response = requests.get(url)
        if response.status_code != 200:
            continue
        data = response.json()
        if not rating or data.get("rating") == rating:
            return data["question"]
    return None


def joke():
    setup = access_api(
        "https://official-joke-api.appspot.com/jokes/random",
        "setup",
        error_messages["joke"],
    )
    punchline = access_api(
        "https://official-joke-api.appspot.com/jokes/random",
        "punchline",
        error_messages["joke"],
    )
    response = f"{setup} ||{punchline}||"
    return response
