from random import choice

import requests

from .data import error_messages, output


def access_api(url, parameter, error_message, headers=None):
    if headers:
        raw = requests.get(url, headers=headers)
    else:
        raw = requests.get(url)
    if raw.status_code == 200:
        try:
            data = raw.json()
            response = data[parameter]
            return (True, response)
        except (requests.exceptions.JSONDecodeError, KeyError):
            return (False, str(error_message))
        except Exception as e:
            return (False, str(f"{error_message} (Error {str(e)})"))
    else:
        return (False, str(f"{error_message} (HTTP {raw.status_code})"))


# ---------- Commands ----------
def quote():
    quote_response = requests.get("https://zenquotes.io/api/random")
    if quote_response.status_code != 200:
        return f"{error_messages['quote']} (HTTP {quote_response.status_code})"
    try:
        data = quote_response.json()
        fetched_quote = data[0]["q"]
        author = data[0]["a"]
        response = (
            choice(output["commands"]["quote"])
            .replace(r"{{QUOTE}}", fetched_quote)
            .replace(r"{{AUTHOR}}", author)
        )
    except (requests.exceptions.JSONDecodeError, KeyError, IndexError):
        response = error_messages["quote"]
    return response


def meme():
    success, url = access_api(
        "https://meme-api.com/gimme", "url", error_messages["meme"]
    )
    if not success:
        return url
    return choice(output["commands"]["meme"]).replace(r"{{URL}}", url)


def waifu():
    success1, waifu1 = access_api(
        "https://api.waifu.pics/sfw/waifu", "url", error_messages["waifu"]
    )
    if not success1:
        return waifu1
    success2, waifu2 = access_api(
        "https://api.waifu.pics/sfw/waifu", "url", error_messages["waifu"]
    )
    if not success2:
        return waifu2
    return (
        choice(output["commands"]["waifu"])
        .replace(r"{{URL1}}", waifu1)
        .replace(r"{{URL2}}", waifu2)
    )


def duck():  # TODO: Fix function (command doesnt respond)
    success, url = access_api(
        "https://random-d.uk/api/random", "url", error_messages["duck"]
    )
    if not success:
        return url
    return choice(output["commands"]["duck"]).replace(r"{{URL}}", url)


def dog():
    success, url = access_api(
        "https://random.dog/woof.json", "url", error_messages["dog"]
    )
    if not success:
        return url
    return choice(output["commands"]["dog"]).replace(r"{{URL}}", url)


def cat():
    raw = requests.get("https://api.thecatapi.com/v1/images/search")
    if raw.status_code != 200:
        return f"{error_messages['cat']} (HTTP {raw.status_code})"
    try:
        data = raw.json()
        response = choice(output["commands"]["cat"]).replace(r"{{URL}}", data[0]["url"])
    except (requests.exceptions.JSONDecodeError, KeyError, IndexError):
        response = error_messages["cat"]
    return response


def chuck():
    success, joke = access_api(
        "https://api.chucknorris.io/jokes/random", "value", error_messages["chuck"]
    )
    if not success:
        return joke
    return choice(output["commands"]["chuck_norris"]).replace(r"{{JOKE}}", joke)


def fact():
    success, fact_text = access_api(
        "https://uselessfacts.jsph.pl/api/v2/facts/random",
        "text",
        error_messages["fact"],
    )
    if not success:
        return fact_text
    return choice(output["commands"]["fact"]).replace(r"{{FACT}}", fact_text)


def bible(
    is_random, book_arg: str = "John", chapter_arg: int = 16, verse_arg: int = 32
):
    if is_random:
        url = "https://bible-api.com/data/web/random"
    else:
        url = f"https://bible-api.com/{book_arg} {chapter_arg}:{verse_arg}"

    bible_response = requests.get(url)
    if bible_response.status_code == 200:
        try:
            data = bible_response.json()
            if "random_verse" in data:
                verse = data["random_verse"]
                response = (
                    choice(output["commands"]["bible"])
                    .replace(r"{{PASSAGE}}", verse["text"])
                    .replace(r"{{BOOK}}", verse["book"])
                    .replace(r"{{CHAPTER}}", str(verse["chapter"]))
                    .replace(r"{{VERSE}}", str(verse["verse"]))
                )
            elif "text" in data and "reference" in data:
                parts = data["reference"].split()
                book = parts[0] if parts else book_arg
                ref_parts = data["reference"].split(":")
                chapter_verse = ref_parts[1] if len(ref_parts) > 1 else "1"
                chapter = (
                    chapter_verse.split(":")[0]
                    if ":" in chapter_verse
                    else chapter_verse
                )
                verse_num = chapter_verse.split(":")[1] if ":" in chapter_verse else "1"
                response = (
                    choice(output["commands"]["bible"])
                    .replace(r"{{PASSAGE}}", data["text"])
                    .replace(r"{{BOOK}}", book)
                    .replace(r"{{CHAPTER}}", chapter)
                    .replace(r"{{VERSE}}", verse_num)
                )
            else:
                response = error_messages["passage_not_found"].replace(
                    r"{{PASSAGE}}", f"{book_arg} {chapter_arg}:{verse_arg}"
                )
        except (requests.exceptions.JSONDecodeError, KeyError):
            response = error_messages["bible"]
    elif bible_response.status_code == 404:
        response = error_messages["passage_not_found"].replace(
            r"{{PASSAGE}}", f"{book_arg} {chapter_arg}:{verse_arg}"
        )
    else:
        response = f"{error_messages['bible']} (HTTP {bible_response.status_code})"
    return response


def bitcoin(currency_parameter):
    currency = currency_parameter.lower() if len(str(currency_parameter)) > 1 else "usd"
    bitcoin_price = requests.get(
        f"https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies={currency}"
    )
    if bitcoin_price.status_code == 200:
        data = bitcoin_price.json()
        if "bitcoin" in data and currency in data["bitcoin"]:
            response = (
                choice(output["commands"]["bitcoin"])
                .replace(r"{{AMOUNT}}", str(data["bitcoin"][currency]))
                .replace(r"{{CURRENCY}}", currency.upper())
            )
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
    raw = requests.get("https://official-joke-api.appspot.com/jokes/random")
    if raw.status_code != 200:
        return f"{error_messages['joke']} (HTTP {raw.status_code})"
    try:
        data = raw.json()
        response = (
            choice(output["commands"]["joke"])
            .replace(r"{{SETUP}}", data["setup"])
            .replace(r"{{PUNCHLINE}}", data["punchline"])
        )
    except (requests.exceptions.JSONDecodeError, KeyError):
        response = error_messages["joke"]
    return response


def currency(currency1, currency2, amount):
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return error_messages["currency"]

    currency1 = currency1.lower()
    currency2 = currency2.lower()

    available_currencies = requests.get(
        "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.json"
    )

    if available_currencies.status_code != 200:
        return error_messages["unavailable"]

    available_currencies = available_currencies.json()

    if currency1 not in available_currencies:
        return f"{error_messages['currency']} ({currency1})"
    if currency2 not in available_currencies:
        return f"{error_messages['currency']} ({currency2})"

    raw_response = requests.get(
        f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{currency1}.json"
    )

    if raw_response.status_code != 200:
        return error_messages["unavailable"]

    raw_response = raw_response.json()

    if currency1 not in raw_response or currency2 not in raw_response[currency1]:
        return error_messages["currency"]

    rate = raw_response[currency1][currency2]
    converted_amount = rate * amount
    response = (
        choice(output["commands"]["currency"])
        .replace(r"{{FROM_AMOUNT}}", str(amount))
        .replace(r"{{FROM_CURRENCY}}", currency1.upper())
        .replace(r"{{TO_AMOUNT}}", f"{converted_amount:.2f}")
        .replace(r"{{TO_CURRENCY}}", currency2.upper())
    )
    return response
