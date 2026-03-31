import requests


# Diese Funktion holt den aktuellen Bitcoin-Preis in USD
# von der CoinGecko API.
def get_bitcoin_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

    response = requests.get(url)

    # Prüfen, ob der Request erfolgreich war
    if response.status_code == 200:
        data = response.json()

        # Preis aus dem JSON holen
        price = data["bitcoin"]["usd"]
        return price

    print("Error while loading Bitcoin price.")
    return None