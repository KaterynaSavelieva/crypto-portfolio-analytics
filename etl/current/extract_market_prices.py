# Import der Hilfsfunktion für API-Anfragen
from utils.api_client import fetch_with_retry


# Diese Funktion holt aktuelle Marktpreise von CoinGecko
def get_market_prices():

    # API URL
    url = "https://api.coingecko.com/api/v3/simple/price"

    # Parameter für die Anfrage:
    # Wir wollen Preise für Bitcoin und Ethereum in USD
    params = {
        "ids": "bitcoin,ethereum",
        "vs_currencies": "usd",
    }

    # API-Aufruf mit Retry-Logik
    data = fetch_with_retry(url, params)

    # Wenn keine Daten zurückkommen
    if data is None:
        print("No data received from API")
        return None

    # Rückgabe der Daten in einfacher Struktur
    return {
        "BTC": data["bitcoin"]["usd"],
        "ETH": data["ethereum"]["usd"],
    }


#Hier lade ich Preise von der API.
# Bitcoin und Ethereum werden in USD geladen.