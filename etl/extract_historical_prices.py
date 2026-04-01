import requests
from datetime import datetime

from utils.api_client import fetch_with_retry

# Diese Funktion holt historische Tagespreise von CoinGecko (BTC, ETH usw.)
def get_historical_prices (coin_id, start_date, end_date):

    # URL für historische Daten (Zeitraum)
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart/range"

    # Start- und Enddatum in Unix-Timestamp umwandeln (Sekunden seit 1970)
    start_timestamp = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
    end_timestamp = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())

    # Parameter für die API-Anfrage
    params = {
        "vs_currency": "eur",   # wir wollen Preise in Euro
        "from": start_timestamp,
        "to": end_timestamp,
    }


    data = fetch_with_retry(url, params)
    if data is None:
        print("Keine historischen Daten erhalten")
        return []

    # Liste für tägliche Preise vorbereiten
    daily_prices = []

    # Durch alle Preis-Daten iterieren
    for price_entry in data['prices']:
        timestamp_ms = price_entry[0]     # Zeit in Millisekunden
        price_eur = price_entry[1]        # Preis in EUR

        # Timestamp → Datum (Format YYYY-MM-DD)
        price_date = datetime.fromtimestamp(timestamp_ms / 1000).strftime("%Y-%m-%d")

        # Ergebnis in Liste speichern
        daily_prices.append({
            "price_date": price_date,
            "price_eur": price_eur
        })

    # Liste mit Tagespreisen zurückgeben
    return daily_prices



