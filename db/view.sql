USE crypto_portfolio_db;

DROP VIEW IF EXISTS v_transactions_overview1;
DROP VIEW IF EXISTS v_transaction_clean;
DROP VIEW IF EXISTS v_portfolio_value_simple;
DROP VIEW IF EXISTS v_market_prices_latest_simple;
DROP VIEW IF EXISTS v_portfolio_balance_simple;
DROP VIEW IF EXISTS v_transactions_overview;

CREATE OR REPLACE VIEW v_transactions_overview AS
SELECT
    t.transaction_id,
    c.client_name,
    p.platform_name,
    a.asset_symbol,
    s.status_name,
    cur.currency_code,
    t.transaction_date,
    t.transaction_type,
    t.amount,
    t.buy_price,
    t.buy_price_eur,
    t.exchange_fee_eur,
    t.service_fee_eur,
    t.referral_bonus_eur
FROM transactions t
JOIN clients c
    ON t.client_id = c.client_id
JOIN platforms p
    ON t.platform_id = p.platform_id
JOIN assets a
    ON t.asset_id = a.asset_id
JOIN statuses s
    ON t.status_id = s.status_id
JOIN currencies cur
    ON t.currency_id = cur.currency_id;

SELECT * FROM v_transactions_overview;


CREATE OR REPLACE VIEW v_portfolio_balance_simple AS
SELECT
    client_name,
    platform_name,
    asset_symbol,
    SUM(
        CASE
            WHEN transaction_type = 'BUY' THEN amount
            WHEN transaction_type = 'SELL' THEN -amount
            ELSE 0
        END
    ) AS net_amount
FROM v_transactions_overview
GROUP BY
    client_name,
    platform_name,
    asset_symbol;

SELECT * 
FROM v_portfolio_balance_simple
ORDER BY client_name, platform_name, asset_symbol;




CREATE OR REPLACE VIEW v_market_prices_latest_simple AS
SELECT
    mp.asset_id,
    a.asset_symbol,
    mp.price_date,
    mp.price_usd,
    mp.eur_rate,
    mp.price_eur
FROM market_prices mp
JOIN assets a
    ON mp.asset_id = a.asset_id
JOIN (
    SELECT
        asset_id,
        MAX(price_date) AS max_price_date
    FROM market_prices
    GROUP BY asset_id
) latest
    ON mp.asset_id = latest.asset_id
   AND mp.price_date = latest.max_price_date;


SELECT * FROM v_market_prices_latest_simple;


CREATE OR REPLACE VIEW v_portfolio_value_simple AS
SELECT
    b.client_name,
    b.platform_name,
    b.asset_symbol,
    b.net_amount,
    p.price_date AS latest_price_date,
    p.price_eur AS latest_price_eur,
    b.net_amount * p.price_eur AS current_value_eur
FROM v_portfolio_balance_simple b
JOIN v_market_prices_latest_simple p
    ON b.asset_symbol = p.asset_symbol;

SELECT * 
FROM v_portfolio_value_simple
ORDER BY client_name, platform_name, asset_symbol;


