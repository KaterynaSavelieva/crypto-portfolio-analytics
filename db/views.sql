USE crypto_portfolio_db;   

CREATE VIEW v_transactions_overview AS
SELECT
    t.transaction_id,
    c.client_name,
    p.platform_name,
    a.asset_symbol,
    s.status_name AS status,
    cur.currency_code AS currency,
    t.transaction_date,
    t.amount,
    t.buy_price,
    t.buy_price_eur,
    t.exchange_fee_eur,
    t.service_fee_eur,
    t.referral_bonus_eur
FROM transactions t
JOIN clients c ON t.client_id = c.client_id
JOIN platforms p ON t.platform_id = p.platform_id
JOIN assets a ON t.asset_id = a.asset_id
JOIN statuses s ON t.status_id = s.status_id
JOIN currencies cur ON t.currency_id = cur.currency_id;
    
SELECT * FROM v_transactions_overview
ORDER BY t.transaction_date;    