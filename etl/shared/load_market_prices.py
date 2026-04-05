# Diese Funktion holt aktuelle Marktpreise von CoinGecko.
def get_asset_ids(connection):
    cursor = connection.cursor(dictionary=True)  # Der Cursor liefert aktuell Tupel zurück.
                                                 # Deshalb muss ich entweder dictionary=True verwenden.

    query = """
    SELECT asset_id, asset_symbol
    FROM assets
    WHERE asset_symbol IN ('BTC', 'ETH')
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()

    asset_map = {}
    for row in rows:
        asset_map[row["asset_symbol"]] = row["asset_id"]

    return asset_map