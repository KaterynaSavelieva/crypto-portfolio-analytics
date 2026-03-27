import pandas as pd


# Diese Funktion lädt die Investment-Daten aus CSV
def load_investments():

    # CSV-Datei wird mit Pandas eingelesen
    #pd.read_csv() ist eine Funktion von Pandas, um CSV-Dateien zu laden.
    df = pd.read_csv("data/investments.csv")

    # DataFrame wird zurückgegeben
    # Ein DataFrame ist wie eine Tabelle in Excel mit Zeilen und Spalten
    return df


# Diese Funktion bereitet die Daten für Analyse vor
def transform_data(df):
    # Datum konvertieren (String → datetime)
    df["date"] = pd.to_datetime(df["date"])
    return df


# Diese Funktion berechnet den aktuellen Wert und Gewinn
def calculate_profit(df, current_price):

    # aktueller Wert der Investition
    df["current_value"] = df["amount"] * current_price

    # ursprünglicher Wert
    df["buy_value"] = df["amount"] * df["buy_price_usd"]

    # Gewinn
    df["profit"] = df["current_value"] - df["buy_value"]

    return df