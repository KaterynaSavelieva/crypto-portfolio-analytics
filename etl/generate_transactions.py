import random
from db.db_connection import create_connection


# Diese Funktion holt alle Marktpreise aus der Datenbank
def get_market_prices(connection):
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT asset_id, price_date, price_usd, price_eur
        FROM market_prices
        ORDER BY price_date
    """)

    rows = cursor.fetchall()
    cursor.close()

    return rows


# Diese Funktion generiert realistische Transaktionen
def generate_transactions():
    # Verbindung zur Datenbank öffnen
    connection = create_connection()
    cursor = connection.cursor()

    # Portfolio speichert: wie viel ein Kunde von einem Asset besitzt
    # key = (client_id, platform_id, asset_id)
    portfolio = {}

    try:
        # Marktpreise laden
        market_prices = get_market_prices(connection)

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
            if random.random() > 0.3:
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
        # Verbindung schließen (immer!)
        cursor.close()
        connection.close()


# Startpunkt - wird nur beim direkten Start ausgeführt
if __name__ == "__main__":
    generate_transactions()