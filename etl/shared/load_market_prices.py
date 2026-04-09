# Diese Funktion holt die Asset-IDs aus der Datenbank
def get_asset_ids(connection):

    # Cursor mit Dictionary-Format (damit wir Namen statt Index verwenden können)
    cursor = connection.cursor(dictionary=True)
    #Ohne dictionary=True bekommt man Tupel statt Spaltennamen.

    # SQL-Abfrage:
    # Wir holen die IDs für BTC und ETH
    query = """
    SELECT asset_id, asset_symbol
    FROM assets
    WHERE asset_symbol IN ('BTC', 'ETH')
    """

    # Abfrage ausführen
    cursor.execute(query)

    # Alle Ergebnisse holen
    rows = cursor.fetchall()

    # Cursor schließen
    cursor.close()

    # Mapping erstellen: Symbol - ID
    asset_map = {}
    for row in rows:
        asset_map[row["asset_symbol"]] = row["asset_id"]

    # Mapping zurückgeben
    return asset_map