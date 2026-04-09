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

select * from market_prices order by price_date desc;


USE crypto_portfolio_db;

SELECT
    t.client_id,
    a.asset_symbol,
    SUM(CASE WHEN t.transaction_type = 'SELL' THEN t.amount ELSE 0 END) AS sell_sum_transactions
FROM transactions t
JOIN assets a ON t.asset_id = a.asset_id
JOIN statuses s ON t.status_id = s.status_id
WHERE s.status_name = 'completed'
  AND t.transaction_date = '2026-04-08'
  AND a.asset_symbol = 'ETH'
GROUP BY t.client_id, a.asset_symbol
ORDER BY t.client_id;

SELECT
    s.client_id,
    a.asset_symbol,
    s.sell_qty_day
FROM portfolio_daily_snapshot s
JOIN assets a ON s.asset_id = a.asset_id
WHERE s.snapshot_date = '2026-04-08'
  AND a.asset_symbol = 'ETH'
ORDER BY s.client_id;

SELECT
    t.client_id,
    t.transaction_type,
    t.transaction_id,
    a.asset_symbol,
    t.amount,
    vto.net_amount
FROM transactions t
JOIN assets a ON t.asset_id = a.asset_id
JOIN statuses s ON t.status_id = s.status_id
JOIN v_transactions_overview vto ON vto.transaction_id = t.transaction_id
WHERE s.status_name = 'completed'
  AND t.transaction_date = '2026-04-08'
  AND a.asset_symbol = 'ETH'
  AND t.client_id = 1
   AND t.transaction_type ='SELL'
-- GROUP BY t.client_id, a.asset_symbol
ORDER BY t.client_id;


