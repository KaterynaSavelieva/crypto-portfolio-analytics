import pandas as pd
from db.db_connection import create_connection
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
from utils.formatter import *

def load_transactions():
    connection = create_connection()

    #Ich habe eine View für die Datenlogik erstellt
    query = """
    SELECT * FROM v_transactions_overview   
    ORDER BY t.transaction_date;
    """

    df = pd.read_sql(query, connection)
    connection.close()
    return df


if __name__ == "__main__":
    df = load_transactions()
    print(df)

    df["total_buy_eur"] = df["amount"] * df["buy_price_eur"]
    df["total_cost_eur"] = df["total_buy_eur"] + df["exchange_fee_eur"] + df["service_fee_eur"] - df[
        "referral_bonus_eur"]

    # Ich formatiere die Spaltennamen im Python-Code für die Benutzeranzeige.
    print_table_titel(prettify(df), "Transactions")