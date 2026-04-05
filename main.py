from etl.current.update_market_prices import update_market_prices
from db.test_select import load_transactions
from utils.formatter import *

def main():
    print("Project started successfully.")
    update_market_prices()

    df = load_transactions()
    print_table_titel(prettify(df), "Transactions")


if __name__ == "__main__":
    main()