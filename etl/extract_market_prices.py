from utils.api_client import fetch_with_retry

# Diese Funktion holt aktuelle Marktpreise von CoinGecko.
def get_market_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": "bitcoin,ethereum",
        "vs_currencies": "eur",
    }


    data = fetch_with_retry(url, params)

    if data is None:
        print("Keine Daten von API erhalten")
        return None

    return {
        "BTC": data["bitcoin"]["eur"],
        "ETH": data["ethereum"]["eur"],
    }
