from datetime import datetime
from utils.exchange_rate_api import get_eur_rate
from etl.current.extract_market_prices import get_market_prices
from etl.shared.load_market_prices import get_asset_ids
from db.db_connection import create_connection
from utils.logger import get_logger

# Das Skript lädt aktuelle BTC- und ETH-Preise aus der API
# und speichert sie in der Tabelle market_prices
def update_market_prices():
    logger = get_logger()
    logger.info("Updating market prices")
    print("Loading current market prices from API...")

    prices = get_market_prices()

    if prices is None:
        print("API error - no prices received")
        return

    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    today = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    eur_rate = get_eur_rate(today[:10])

    if eur_rate is None:
        print("No exchange rate received")
        return

    connection = create_connection()
    cursor = connection.cursor()

    try:
        asset_map = get_asset_ids(connection)
        logger.info("Asset IDs:", asset_map)
        #print("Asset IDs:", asset_map)

        for symbol, price_usd in prices.items():
            asset_id = asset_map[symbol]
            price_eur = price_usd * eur_rate

            cursor.execute("""
                INSERT INTO market_prices (asset_id, price_date, price_usd, eur_rate, price_eur)
                VALUES (%s, %s, %s, %s, %s)
            """, (asset_id, today, price_usd, eur_rate, price_eur))

            logger.info(f"Saved {symbol}: price_usd={price_usd}, eur_rate={eur_rate}, price_eur={price_eur:.8f}")

        connection.commit()
        #print("Current market prices saved successfully.")
        logger.info("Current market prices saved successfully.")

    except Exception as e:
        connection.rollback()
        logger.exception(f"Error while saving market prices: {e}")
        raise


    finally:
        cursor.close()
        connection.close()