from etl.extract import get_bitcoin_price
from etl.transform import load_investments
from etl.transform import transform_data
from etl.transform import calculate_profit
import pandas as pd
from tabulate import tabulate
from utils.formatter import *

#Diese Einstellungen sorgen dafür, dass alle Spalten vollständig angezeigt werden.
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


# Startpunkt des Programms
def main():
    print("Project started successfully.")

    bitcoin_price = get_bitcoin_price()
    print("Current Bitcoin price in USD:", bitcoin_price)

    # CSV laden
    df = load_investments()
    print_header("Information before transform:")
    df.info()

    df = transform_data(df)
    print_table_titel(df, "Investments Data")

    print_header("Information after transform")
    df.info()# df.info() zeigt Struktur der Daten
            # Achtung: Diese Methode gibt None zurück!

    df = calculate_profit(df, bitcoin_price)
    print_header("Information after calculation")
    df.info()
    print_table_titel(df, "Analysis")





if __name__ == "__main__":
    main()