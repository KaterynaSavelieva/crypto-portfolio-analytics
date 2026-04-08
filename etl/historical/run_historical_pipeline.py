from etl.historical.update_historical_prices import update_historical_prices
from etl.shared.generate_transactions import generate_transactions
from utils.formatter import print_header
from utils.logger import get_logger


def run_historical_pipeline():
    #start_date = "2025-04-10"
    #end_date = "2026-04-05"

    logger = get_logger()
    start_date = "2026-04-07"
    end_date = "2026-04-07"

    try:
        logger.info(f"Starting pipeline for {start_date} to {end_date}")
        print_header("HISTORICAL PIPELINE START")

        # 1. historische Preise laden
        update_historical_prices(start_date, end_date)
        logger.info(f"Historical prices updated for period {start_date} to {end_date}")

        # 2. Transaktionen für Zeitraum generieren
        generate_transactions(start_date, end_date, use_random=True)
        logger.info(f"Transactions generated for period {start_date} to {end_date}")

        print_header("HISTORICAL PIPELINE FINISHED")
        logger.info(f"Historical prices saved for period {start_date} to {end_date}")

    except Exception as e:
        logger.exception(f"HISTORICAL PIPELINE FAILED: {e}")
        raise


if __name__ == "__main__":
    run_historical_pipeline()