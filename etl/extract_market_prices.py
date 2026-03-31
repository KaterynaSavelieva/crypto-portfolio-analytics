import requests


# Diese Funktion holt aktuelle Marktpreise von CoinGecko.
def get_market_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum",
        "vs_currencies": "eur",
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    return {
        "BTC": data["bitcoin"]["eur"],
        "ETH": data["ethereum"]["eur"],
    }
