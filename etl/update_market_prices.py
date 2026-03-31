from etl.extract_market_prices import get_market_prices
from etl.load_market_prices import get_asset_ids, save_market_prices
from db.db_connection import create_connection

#Das Skript lädt aktuelle BTC- und ETH-Preise aus der API
# und speichert sie in der Tabelle market_prices

def update_market_prices():
    print("Loading market prices from API...")
    prices = get_market_prices()

    connection = create_connection()
    try:
        asset_map = get_asset_ids(connection)
        print("Asset IDs: ", asset_map)

        save_market_prices (connection, prices, asset_map)
        print("Market prices saved successfully .")
    finally:
        connection.close()

if __name__ == "__main__":
    update_market_prices()
