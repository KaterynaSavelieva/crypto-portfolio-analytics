from utils.exchange_rate_api import get_eur_rate
from db.db_connection import create_connection
from etl.historical.extract_historical_prices import get_historical_prices
from etl.shared.load_market_prices import get_asset_ids


# Diese Funktion speichert historische Preise mit USD, EUR-Kurs und EUR-Preis.
def update_prices_with_eur(connection, asset_id, prices):
    cursor = connection.cursor()

    for row in prices:
        # Datum direkt aus dem Dictionary holen
        date = row["price_date"]

        # USD-Preis aus den historischen Daten holen
        price_usd = row["price_usd"]

        # EUR-Kurs für dieses Datum holen (api frankfurt)
        eur_rate = get_eur_rate(date)

        # Wenn kein Kurs gefunden wurde, diesen Tag überspringen
        if eur_rate is None:
            print(f"Kein EUR-Kurs für {date} gefunden")
            continue

        # EUR-Preis berechnen
        price_eur = price_usd * eur_rate

        # Datensatz in die Tabelle market_prices speichern
        cursor.execute("""
            INSERT INTO market_prices (asset_id, price_date, price_usd, eur_rate, price_eur)
            VALUES (%s, %s, %s, %s, %s)
        """, (asset_id, date, price_usd, eur_rate, price_eur))

    # Alle Änderungen speichern
    connection.commit()

    # Cursor schließen
    cursor.close()


# Diese Funktion lädt historische Preise und speichert sie in der Datenbank.
def update_historical_prices(start_date, end_date):
    print("Loading historical market prices...")

    connection = create_connection()

    try:
        # Asset-IDs aus der Datenbank laden, z. B. BTC -> 1, ETH -> 2
        asset_map = get_asset_ids(connection)
        print("Asset map:", asset_map)

        # Historische BTC-Daten laden
        btc_prices = get_historical_prices("bitcoin", start_date, end_date)
        print("BTC prices loaded:", len(btc_prices))

        # Historische ETH-Daten laden
        eth_prices = get_historical_prices("ethereum", start_date, end_date)
        print("ETH prices loaded:", len(eth_prices))

        # BTC mit USD, EUR-Kurs und EUR-Preis speichern
        update_prices_with_eur(connection, asset_map["BTC"], btc_prices)
        print("BTC saved with EUR data")

        # ETH mit USD, EUR-Kurs und EUR-Preis speichern
        update_prices_with_eur(connection, asset_map["ETH"], eth_prices)
        print("ETH saved with EUR data")

        print("Historical prices saved successfully")

    finally:
        # Verbindung immer schließen
        connection.close()


