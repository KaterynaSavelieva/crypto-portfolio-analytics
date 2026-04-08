USE crypto_portfolio_db;

show full tables  where table_type="VIEW";

select * from transactions order by  transaction_id desc;

select count(*) from transactions;

select * from v_transactions_overview order by transaction_id desc;

select * from v_portfolio_value_simple;

select * from v_market_prices_latest_simple;

select * from v_portfolio_balance_simple;

select * from market_prices order by price_date desc;

select * from statuses;

UPDATE transactions SET status_id = 2 WHERE status_id = 1;

select * from market_prices order by price_date;

