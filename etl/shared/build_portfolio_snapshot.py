#Hier wird der Portfolio-Snapshot aufgebaut.
# Aus Transaktionen und Marktpreisen werden Kennzahlen für das Dashboard berechnet.
#Dieser Schritt ist besonders wichtig,weil hier aus Rohdaten analysierbare Kennzahlen entstehen.
# BUY erhöht den Bestand
# SELL reduziert den Bestand
# danach werden Value und Profit berechnet

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Dict, Tuple

import pandas as pd

from db.db_connection import create_connection
from utils.logger import get_logger


# Logger für dieses Modul
logger = get_logger("portfolio_snapshot")


# Diese Klasse speichert den aktuellen Portfolio-Zustand
@dataclass
class PortfolioState:
    balance_qty: Decimal = Decimal("0")
    avg_buy_price_eur: Decimal = Decimal("0")


# Hilfsfunktion:
# Wandelt einen Wert sicher in Decimal um
def to_decimal(value: object) -> Decimal:
    if value is None:
        return Decimal("0")
    return Decimal(str(value))


# Diese Funktion lädt die Transaktionen aus einer View
def load_transactions(connection) -> pd.DataFrame:
    query = """
        SELECT
            transaction_id,
            transaction_date,
            client_id,
            asset_id,
            transaction_type,
            amount,
            price_eur
        FROM v_transactions_for_snapshot
        ORDER BY transaction_date, transaction_id
    """
    return pd.read_sql(query, connection)


# Diese Funktion lädt tägliche Marktpreise aus einer View
def load_daily_market_prices(connection) -> pd.DataFrame:
    query = """
        SELECT
            snapshot_date,
            asset_id,
            market_price_eur
        FROM v_daily_market_prices_for_snapshot
        ORDER BY snapshot_date, asset_id
    """
    return pd.read_sql(query, connection)


# Diese Funktion baut den Snapshot als DataFrame auf
def build_snapshot_dataframe(
    transactions_df: pd.DataFrame,
    market_prices_df: pd.DataFrame,
) -> pd.DataFrame:

    # Mapping für Marktpreise pro Datum und Asset
    market_price_map: Dict[Tuple[date, int], Decimal] = {}

    for _, row in market_prices_df.iterrows():
        key = (pd.to_datetime(row["snapshot_date"]).date(), int(row["asset_id"]))
        market_price_map[key] = to_decimal(row["market_price_eur"])

    # Aktueller Zustand pro Kunde und Asset
    states: Dict[Tuple[int, int], PortfolioState] = {}

    # Tägliche Snapshot-Daten
    daily_snapshots: Dict[Tuple[date, int, int], dict] = {}

    # Durch alle Transaktionen gehen
    for _, row in transactions_df.iterrows():

        snapshot_date = pd.to_datetime(row["transaction_date"]).date()
        client_id = int(row["client_id"])
        asset_id = int(row["asset_id"])

        transaction_type = row["transaction_type"]
        amount = to_decimal(row["amount"])
        price_eur = to_decimal(row["price_eur"])

        state_key = (client_id, asset_id)
        old_state = states.get(state_key, PortfolioState())

        old_balance = old_state.balance_qty
        old_avg = old_state.avg_buy_price_eur

        realized_profit_day = Decimal("0")
        buy_qty_day = Decimal("0")
        sell_qty_day = Decimal("0")

        new_balance = old_balance
        new_avg = old_avg

        # BUY: Bestand erhöhen und neuen Durchschnitt berechnen
        if transaction_type == "BUY":
            buy_qty_day = amount
            new_balance = old_balance + amount

            if new_balance > 0:
                new_avg = ((old_balance * old_avg) + (amount * price_eur)) / new_balance

        # SELL: Bestand reduzieren und realisierten Gewinn berechnen
        elif transaction_type == "SELL":
            sell_qty_day = amount

            # Gewinn wird mit dem alten Durchschnittspreis berechnet
            realized_profit_day = (amount * price_eur) - (amount * old_avg)

            new_balance = old_balance - amount

            if new_balance == 0:
                new_avg = Decimal("0")
            else:
                new_avg = old_avg

        # Sicherheitsprüfung: negativer Bestand
        if new_balance < 0:
            logger.warning(
                "Negative balance detected for client_id=%s asset_id=%s on %s",
                client_id,
                asset_id,
                snapshot_date,
            )

        # Marktpreis für dieses Datum holen
        market_price = market_price_map.get((snapshot_date, asset_id), Decimal("0"))

        # Kennzahlen berechnen
        book_value = new_balance * new_avg
        market_value = new_balance * market_price
        unrealized_profit = market_value - book_value

        # Aktuellen Zustand speichern
        states[state_key] = PortfolioState(
            balance_qty=new_balance,
            avg_buy_price_eur=new_avg,
        )

        # Schlüssel für täglichen Snapshot
        daily_key = (snapshot_date, client_id, asset_id)

        # Wenn noch kein Eintrag für diesen Tag existiert, neu anlegen
        if daily_key not in daily_snapshots:
            daily_snapshots[daily_key] = {
                "snapshot_date": snapshot_date,
                "client_id": client_id,
                "asset_id": asset_id,
                "buy_qty_day": Decimal("0"),
                "sell_qty_day": Decimal("0"),
                "balance_qty": Decimal("0"),
                "avg_buy_price_eur": Decimal("0"),
                "book_value_eur": Decimal("0"),
                "market_price_eur": Decimal("0"),
                "market_value_eur": Decimal("0"),
                "realized_profit_day_eur": Decimal("0"),
                "unrealized_profit_eur": Decimal("0"),
            }

        # Werte für den Tag speichern
        daily_snapshots[daily_key]["buy_qty_day"] += buy_qty_day
        daily_snapshots[daily_key]["sell_qty_day"] += sell_qty_day
        daily_snapshots[daily_key]["balance_qty"] = new_balance
        daily_snapshots[daily_key]["avg_buy_price_eur"] = new_avg
        daily_snapshots[daily_key]["book_value_eur"] = book_value
        daily_snapshots[daily_key]["market_price_eur"] = market_price
        daily_snapshots[daily_key]["market_value_eur"] = market_value
        daily_snapshots[daily_key]["realized_profit_day_eur"] += realized_profit_day
        daily_snapshots[daily_key]["unrealized_profit_eur"] = unrealized_profit

    # Snapshot als DataFrame zurückgeben
    return pd.DataFrame(daily_snapshots.values())


# Diese Funktion löscht alte Snapshot-Daten
def clear_snapshot_table(connection) -> None:
    cursor = connection.cursor()
    cursor.execute("DELETE FROM portfolio_daily_snapshot")
    connection.commit()
    cursor.close()


# Diese Funktion speichert den neuen Snapshot in der Datenbank
def insert_snapshot_dataframe(connection, snapshot_df: pd.DataFrame) -> None:
    insert_sql = """
        INSERT INTO portfolio_daily_snapshot (
            snapshot_date,
            client_id,
            asset_id,
            buy_qty_day,
            sell_qty_day,
            balance_qty,
            avg_buy_price_eur,
            book_value_eur,
            market_price_eur,
            market_value_eur,
            realized_profit_day_eur,
            unrealized_profit_eur
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor = connection.cursor()

    # Alle Zeilen aus dem DataFrame in die Datenbank schreiben
    for _, row in snapshot_df.iterrows():
        cursor.execute(
            insert_sql,
            (
                row["snapshot_date"],
                int(row["client_id"]),
                int(row["asset_id"]),
                float(row["buy_qty_day"]),
                float(row["sell_qty_day"]),
                float(row["balance_qty"]),
                float(row["avg_buy_price_eur"]),
                float(row["book_value_eur"]),
                float(row["market_price_eur"]),
                float(row["market_value_eur"]),
                float(row["realized_profit_day_eur"]),
                float(row["unrealized_profit_eur"]),
            ),
        )

    connection.commit()
    cursor.close()


# Hauptfunktion:
# lädt Daten, baut Snapshot und speichert ihn
def main() -> None:
    logger.info("Starting portfolio daily snapshot build")

    connection = create_connection()

    try:
        transactions_df = load_transactions(connection)
        market_prices_df = load_daily_market_prices(connection)

        snapshot_df = build_snapshot_dataframe(transactions_df, market_prices_df)

        clear_snapshot_table(connection)
        insert_snapshot_dataframe(connection, snapshot_df)

        logger.info("portfolio_daily_snapshot updated successfully")

    finally:
        connection.close()


# Startpunkt, wenn die Datei direkt ausgeführt wird
if __name__ == "__main__":
    main()