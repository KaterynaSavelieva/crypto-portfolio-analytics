# Import der Hilfsfunktion für API-Anfragen
from utils.api_client import fetch_with_retry

# Import für Datum (optional für weitere Logik)
from datetime import datetime, timedelta


# Diese Funktion holt den EUR-Kurs für ein bestimmtes Datum (USD - EUR)
# Dieser wird später für die Berechnung verwendet.
def get_eur_rate(date):

    # API URL mit Datum
    url = "https://api.frankfurter.dev/v1/" + date

    # Parameter:
    # Basis ist USD, wir wollen EUR
    params = {
        "base": "USD",
        "symbols": "EUR"
    }

    # API-Aufruf mit Retry-Logik
    data = fetch_with_retry(url, params=params)

    # Wenn keine Daten zurückkommen
    if data is None:
        print("No exchange rate data received")
        return None

    # Rückgabe des EUR-Kurses
    return data["rates"]["EUR"]



def get_eur_rates_for_period(start_date, end_date):
    rates = {}

    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")

        eur_rate = get_eur_rate(date_str)

        rates[date_str] = eur_rate

        current_date += timedelta(days=1)

    return rates


