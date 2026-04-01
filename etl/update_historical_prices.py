from  db.db_connection import create_connection
from etl.extract_historical_prices import get_historical_prices
from etl.load_market_prices import get_asset_ids, save_historical_prices

# Diese Funktion lädt historische Preise und speichert sie in der Datenbank.
def update_historical_prices():
    print("Loading historical market prices...")

    connection = create_connection()

    try:
        asset_map =get_asset_ids(connection)

        btc_prices = get_historical_prices("bitcoin", "2025-01-01", "2025-04-01")
        eth_prices = get_historical_prices("ethereum", "2025-01-01", "2025-04-01")

        save_historical_prices(connection, btc_prices, asset_map["BTC"])
        save_historical_prices(connection, eth_prices, asset_map["ETH"])

        print("Historical prices saved successfully")

    finally:
        connection.close()

    #Diese Bedingung sorgt dafür, dass die Funktion nur beim direkten Start ausgeführt wird
    # und nicht beim Import im Hauptprogramm.
    if __name__ == "__main__":
        update_historical_prices()