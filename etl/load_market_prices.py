
# Diese Funktion holt aktuelle Marktpreise von CoinGecko.
def get_asset_ids(connection):
    cursor = connection.cursor(dictionary=True)  #Der Cursor liefert aktuell Tupel zurück.
                                                #Deshalb muss ich entweder dictionary=True verwenden.

    query = """
    SELECT asset_id, asset_symbol
    FROM assets
    WHERE asset_symbol IN ('BTC', 'ETH')
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()

    asset_map ={}
    for row in rows:
        asset_map[row["asset_symbol"]] = row["asset_id"]
    return asset_map

# Diese Funktion speichert Preise in market_prices.
def save_market_prices (connection, prices, asset_map):
    cursor = connection.cursor()
    query = """
    INSERT INTO market_prices(asset_id, price_date, price_eur)
    VALUES (%s, NOW(), %s)
    """
    for symbol, price in prices.items():
        asset_id = asset_map[symbol]
        cursor.execute(query, (asset_id, price))

    connection.commit()
    cursor.close()


# Diese Funktion speichert historische Tagespreise in market_prices.
def save_historical_prices (connection, historical_prices, asset_id):
    cursor = connection.cursor()

    query = """
    INSERT INTO market_prices(asset_id, price_date, price_eur)
    VALUES (%s, %s, %s)
    """

    for price_entry in historical_prices:
        price_date =price_entry["price_date"]
        price_eur = price_entry["price_eur"]

        cursor.execute(query, (asset_id, price_date, price_eur))

    connection.commit()
    cursor.close()