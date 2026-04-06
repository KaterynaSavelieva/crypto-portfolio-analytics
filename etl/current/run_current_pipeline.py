from datetime import datetime
from etl.current.update_market_prices import update_market_prices
from etl.shared.generate_transactions import generate_transactions
from utils.formatter import print_header


def run_current_pipeline():
    today = datetime.today().strftime("%Y-%m-%d")

    print_header("CURRENT PIPELINE START")

    # 1. aktuelle Preise laden
    update_market_prices()

    # 2. Transaktionen nur für heute generieren
    generate_transactions(today, today, use_random=True)

    print_header("CURRENT PIPELINE FINISHED")


if __name__ == "__main__":
    run_current_pipeline()