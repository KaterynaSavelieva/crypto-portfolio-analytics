from etl.historical.update_historical_prices import update_historical_prices
from etl.shared.generate_transactions import generate_transactions
from utils.formatter import print_header


def run_historical_pipeline():
    start_date = "2025-04-10"
    end_date = "2026-04-05"

    print_header("HISTORICAL PIPELINE START")

    # 1. historische Preise laden
    update_historical_prices(start_date, end_date)

    # 2. Transaktionen für Zeitraum generieren
    generate_transactions(start_date, end_date, use_random=True)

    print_header("HISTORICAL PIPELINE FINISHED")


if __name__ == "__main__":
    run_historical_pipeline()