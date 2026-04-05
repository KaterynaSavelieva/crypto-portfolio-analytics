from datetime import datetime
from utils.exchange_rate_api import get_eur_rate
from etl.current.extract_market_prices import get_market_prices
from etl.shared.load_market_prices import get_asset_ids
from db.db_connection import create_connection

# Das Skript lädt aktuelle BTC- und ETH-Preise aus der API
# und speichert sie in der Tabelle market_prices
def update_market_prices():
    print("Loading current market prices from API...")

    prices = get_market_prices()

    if prices is None:
        print("API error - no prices received")
        return

    today = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    eur_rate = get_eur_rate(today[:10])

    if eur_rate is None:
        print("No exchange rate received")
        return

    connection = create_connection()
    cursor = connection.cursor()

    try:
        asset_map = get_asset_ids(connection)
        print("Asset IDs:", asset_map)

        for symbol, price_usd in prices.items():
            asset_id = asset_map[symbol]
            price_eur = price_usd * eur_rate

            cursor.execute("""
                INSERT INTO market_prices (asset_id, price_date, price_usd, eur_rate, price_eur)
                VALUES (%s, %s, %s, %s, %s)
            """, (asset_id, today, price_usd, eur_rate, price_eur))

        connection.commit()
        print("Current market prices saved successfully.")

    finally:
        cursor.close()
        connection.close()