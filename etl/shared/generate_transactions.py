import random
from db.db_connection import create_connection


# Diese Funktion holt alle Marktpreise aus der Datenbank
def get_market_prices(connection, start_date=None, end_date=None):
    cursor = connection.cursor(dictionary=True)

    # Basis-Query
    query = """
        SELECT asset_id, price_date, price_usd, price_eur
        FROM market_prices
    """

    # Wenn Zeitraum angegeben ist - WHERE hinzufügen
    if start_date and end_date:
        query += " WHERE DATE(price_date) BETWEEN %s AND %s"

    query += " ORDER BY price_date"

    # Query ausführen
    if start_date and end_date:
        cursor.execute(query, (start_date, end_date))
    else:
        cursor.execute(query)

    rows = cursor.fetchall()
    cursor.close()

    return rows


# Diese Funktion generiert realistische Transaktionen
def generate_transactions(start_date=None, end_date=None, use_random=True):
    # Verbindung zur Datenbank öffnen
    connection = create_connection()
    cursor = connection.cursor()

    # Portfolio speichert: wie viel ein Kunde von einem Asset besitzt
    # key = (client_id, platform_id, asset_id)
    portfolio = {}

    try:
        # Marktpreise laden (mit Zeitraum, falls angegeben)
        market_prices = get_market_prices(connection, start_date, end_date)

        # Beispiel IDs (Demo-Daten)
        client_ids = [1, 2, 3, 4, 5, 6]
        platform_ids = [1, 2, 3]
        status_ids = [1, 2]

        # Durch alle Preise iterieren
        for row in market_prices:
            asset_id = row["asset_id"]
            date = row["price_date"]
            price_usd = float(row["price_usd"])
            price_eur = float(row["price_eur"])

            # Nur ca. 30% der Daten verwenden (nicht zu viele Transaktionen)
            if use_random and random.random() > 0.3:
                continue

            # Zufällige Auswahl
            client_id = random.choice(client_ids)
            platform_id = random.choice(platform_ids)
            status_id = random.choice(status_ids)

            key = (client_id, platform_id, asset_id)

            # aktuellen Bestand holen (wenn keiner - 0)
            current_balance = portfolio.get(key, 0)

            # Wenn kein Bestand - nur BUY möglich
            if current_balance == 0:
                transaction_type = "BUY"
            else:
                transaction_type = random.choice(["BUY", "SELL"])

            # Menge je nach Asset (BTC kleiner, ETH größer)
            if asset_id == 1:  # BTC
                min_amount = 0.001
                max_amount = 0.05
            else:              # ETH
                min_amount = 0.01
                max_amount = 0.5

            # BUY - normale Menge generieren
            if transaction_type == "BUY":
                amount = round(random.uniform(min_amount, max_amount), 4)

            # SELL - nur aus vorhandenem Bestand
            else:
                sell_max = min(max_amount, current_balance)

                # Wenn Bestand sehr klein ist - alles verkaufen
                if sell_max < min_amount:
                    amount = round(current_balance, 4)
                else:
                    amount = round(random.uniform(min_amount, sell_max), 4)

            # Preis leicht variieren (realistisch)
            if transaction_type == "BUY":
                factor = random.uniform(1.001, 1.01)   # etwas teurer
            else:
                factor = random.uniform(0.99, 0.999)   # etwas günstiger

            price_usd_tx = round(price_usd * factor, 2)
            price_eur_tx = round(price_eur * factor, 2)

            # Portfolio aktualisieren
            if transaction_type == "BUY":
                portfolio[key] = current_balance + amount
            else:
                portfolio[key] = current_balance - amount

            # Daten in DB speichern
            cursor.execute("""
                INSERT INTO transactions (
                    client_id, platform_id, asset_id, status_id,
                    transaction_date, amount, buy_price, currency_id,
                    buy_price_eur, exchange_fee_eur, service_fee_eur,
                    referral_bonus_eur, transaction_type
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                client_id,
                platform_id,
                asset_id,
                status_id,
                date,
                amount,
                price_usd_tx,
                1,  # currency_id = 1 (USD)
                price_eur_tx,
                round(random.uniform(2, 10), 2),  # exchange fee
                round(random.uniform(1, 5), 2),   # service fee
                round(random.uniform(0, 3), 2),   # referral bonus
                transaction_type
            ))

        # Änderungen speichern
        connection.commit()
        print("Realistic transactions were created")

    finally:
        # Verbindung schließen
        cursor.close()
        connection.close()