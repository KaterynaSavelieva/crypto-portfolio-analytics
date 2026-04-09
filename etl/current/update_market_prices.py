# Import von Datum und Zeit
from datetime import datetime

# Import der Funktion für den Wechselkurs
from utils.exchange_rate_api import get_eur_rate

# Import der Funktion für aktuelle Marktpreise
from etl.current.extract_market_prices import get_market_prices

# Import der Hilfsfunktion für Asset-IDs
from etl.shared.load_market_prices import get_asset_ids

# Import der Datenbankverbindung
from db.db_connection import create_connection

# Import des Loggers
from utils.logger import get_logger


# Dieses Skript lädt aktuelle BTC- und ETH-Preise aus der API
# und speichert sie in der Tabelle market_prices
def update_market_prices():

    # Logger starten
    logger = get_logger()
    logger.info("Updating market prices")

    # Info für den Benutzer
    print("Loading current market prices from API...")

    # Schritt 1: Aktuelle Preise laden
    prices = get_market_prices()

    # Prüfen, ob Daten vorhanden sind
    if prices is None:
        print("API error - no prices received")
        return

    # Aktuelles Datum und Uhrzeit speichern
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    today = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    # Schritt 2: Wechselkurs USD - EUR laden
    eur_rate = get_eur_rate(today[:10])

    # Prüfen, ob Wechselkurs vorhanden ist
    if eur_rate is None:
        print("No exchange rate received")
        return

    # Schritt 3: Verbindung zur Datenbank aufbauen
    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Asset-IDs aus der Datenbank holen
        asset_map = get_asset_ids(connection)
        logger.info("Asset IDs:", asset_map)

        # Schritt 4: Für jedes Asset Preis in EUR berechnen und speichern
        for symbol, price_usd in prices.items():
            asset_id = asset_map[symbol]
            price_eur = price_usd * eur_rate

            cursor.execute("""
                INSERT INTO market_prices (asset_id, price_date, price_usd, eur_rate, price_eur)
                VALUES (%s, %s, %s, %s, %s)
            """, (asset_id, today, price_usd, eur_rate, price_eur))

            logger.info(f"Saved {symbol}: price_usd={price_usd}, eur_rate={eur_rate}, price_eur={price_eur:.8f}")

        # Änderungen speichern
        connection.commit()
        logger.info("Current market prices saved successfully.")

    except Exception as e:
        # Bei Fehler: Änderungen zurücksetzen
        connection.rollback()
        logger.exception(f"Error while saving market prices: {e}")
        raise

    finally:
        # Datenbankverbindung schließen
        cursor.close()
        connection.close()