from datetime import datetime
from etl.current.update_market_prices import update_market_prices
from etl.shared.generate_transactions import generate_transactions
from utils.formatter import print_header
from utils.logger import get_logger




def run_current_pipeline():
    logger = get_logger("current_pipeline")
    today = datetime.today().strftime("%Y-%m-%d")

    try:
        logger.info(f"Starting current pipeline")
        print_header("CURRENT PIPELINE START")

        # 1. aktuelle Preise laden
        update_market_prices()
        logger.info("Current market prices updated successfully")

        # 2. Transaktionen nur für heute generieren
        generate_transactions(today, today, use_random=False)
        logger.info(f"Transactions for today generated successfully")

        print_header("CURRENT PIPELINE FINISHED")
        logger.info(f"Finished current pipeline")

    except Exception as e:
        logger.exception(e)(f"Current pipeline failed: {e}")
        raise


if __name__ == "__main__":
    run_current_pipeline()