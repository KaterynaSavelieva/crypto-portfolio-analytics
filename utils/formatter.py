from tabulate import tabulate

def print_table(df):
    print(tabulate(df, headers='keys', tablefmt='plain'))


def print_header(title):
    print(f"\n======={title}=======")

def print_table_titel(df, title):
   table_str = tabulate(df, headers='keys', tablefmt='plain',showindex=False)
   width =len(table_str.split('\n')[0])     # Breite der Tabelle

   print("\n"+"="*width)
   print(title.center(width))
   print("="*width)

   print (table_str)
   print("="*width+"\n")


def prettify(df):
    return df.rename(columns={
        "transaction_id": "ID",
        "client_name": "Customer",
        "platform_name": "Platform",
        "asset_symbol": "Asset",
        "status_name": "Status",
        "currency_code": "Currency",
        "transaction_date": "Date",
        "amount": "Amount",
        "buy_price": "Buy Price",
        "buy_price_eur": "Buy Price (EUR)",
        "exchange_fee_eur": "Exchange Fee",
        "service_fee_eur": "Service Fee",
        "referral_bonus_eur": "Referral Bonus",
        "total_buy_eur": "Total Investment (EUR)",
        "total_cost_eur": "Total Cost (EUR)",
    })