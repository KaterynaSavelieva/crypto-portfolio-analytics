USE crypto_portfolio_db;

DROP VIEW IF EXISTS v_client_asset_daily;
DROP VIEW IF EXISTS v_portfolio_summary;
DROP VIEW IF EXISTS v_market_prices_latest_simple;
DROP VIEW IF EXISTS v_daily_last_market_prices;
DROP VIEW IF EXISTS v_transactions_overview;


CREATE OR REPLACE VIEW v_transactions_overview AS
SELECT
    t.transaction_id,
    t.client_id,
    c.client_name,
    t.asset_id,
    a.asset_symbol,
    t.transaction_date,
    t.transaction_type,
    CASE
        WHEN t.transaction_type = 'BUY' THEN t.amount
        WHEN t.transaction_type = 'SELL' THEN -t.amount
        ELSE 0
    END AS net_amount,
    t.amount,
    t.buy_price,
    t.buy_price_eur,
    t.exchange_fee_eur,
    t.service_fee_eur,
    t.referral_bonus_eur
FROM transactions t
JOIN clients c
    ON t.client_id = c.client_id
JOIN assets a
    ON t.asset_id = a.asset_id
JOIN statuses s
    ON t.status_id = s.status_id
WHERE s.status_name = 'completed';


CREATE OR REPLACE VIEW v_market_prices_latest_simple AS
SELECT
    mp.asset_id,
    a.asset_symbol,
    mp.price_date,
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


CREATE OR REPLACE VIEW v_daily_last_market_prices AS
SELECT
    DATE(mp.price_date) AS price_day,
    mp.asset_id,
    mp.price_date,
    mp.price_eur
FROM market_prices mp
JOIN (
    SELECT
        asset_id,
        DATE(price_date) AS price_day,
        MAX(price_date) AS last_price_datetime
    FROM market_prices
    GROUP BY asset_id, DATE(price_date)
) latest
    ON mp.asset_id = latest.asset_id
   AND DATE(mp.price_date) = latest.price_day
   AND mp.price_date = latest.last_price_datetime;


CREATE OR REPLACE VIEW v_portfolio_summary AS
SELECT
    t.client_id,
    t.client_name,
    t.asset_id,
    t.asset_symbol,
    SUM(t.net_amount) AS net_amount,
    SUM(CASE
            WHEN t.transaction_type = 'BUY' THEN t.amount * t.buy_price_eur
            ELSE 0
        END)
    / NULLIF(SUM(CASE
                    WHEN t.transaction_type = 'BUY' THEN t.amount
                    ELSE 0
                 END), 0) AS avg_buy_price_eur,
    p.price_date,
    p.price_eur AS market_price_eur,
    SUM(t.net_amount) *
    (
        SUM(CASE
                WHEN t.transaction_type = 'BUY' THEN t.amount * t.buy_price_eur
                ELSE 0
            END)
        / NULLIF(SUM(CASE
                        WHEN t.transaction_type = 'BUY' THEN t.amount
                        ELSE 0
                     END), 0)
    ) AS book_value_eur,
    SUM(t.net_amount) * p.price_eur AS market_value_eur,
    SUM(t.exchange_fee_eur + t.service_fee_eur) AS total_fees_eur,
    SUM(t.referral_bonus_eur) AS total_bonus_eur,
    COUNT(t.transaction_id) AS total_transactions,
    SUM(t.service_fee_eur) AS company_profit_eur,
    (SUM(t.net_amount) * p.price_eur)
    -
    (
        SUM(t.net_amount) *
        (
            SUM(CASE
                    WHEN t.transaction_type = 'BUY' THEN t.amount * t.buy_price_eur
                    ELSE 0
                END)
            / NULLIF(SUM(CASE
                            WHEN t.transaction_type = 'BUY' THEN t.amount
                            ELSE 0
                         END), 0)
        )
    )
    - SUM(t.exchange_fee_eur + t.service_fee_eur)
    + SUM(t.referral_bonus_eur) AS client_profit_eur
FROM v_transactions_overview t
JOIN v_market_prices_latest_simple p
    ON t.asset_id = p.asset_id
GROUP BY
    t.client_id,
    t.client_name,
    t.asset_id,
    t.asset_symbol,
    p.price_date,
    p.price_eur
HAVING SUM(t.net_amount) > 0;


CREATE OR REPLACE VIEW v_client_asset_daily AS
WITH daily_base AS (
    SELECT
        t.client_id,
        c.client_name,
        t.asset_id,
        a.asset_symbol,
        t.transaction_date,
        SUM(CASE
                WHEN t.transaction_type = 'BUY' THEN t.amount
                ELSE 0
            END) AS buy_qty,
        SUM(CASE
                WHEN t.transaction_type = 'SELL' THEN t.amount
                ELSE 0
            END) AS sell_qty,
        SUM(CASE
                WHEN t.transaction_type = 'BUY' THEN t.amount * t.buy_price_eur
                ELSE 0
            END) AS buy_value
    FROM transactions t
    JOIN clients c
        ON t.client_id = c.client_id
    JOIN assets a
        ON t.asset_id = a.asset_id
    JOIN statuses s
        ON t.status_id = s.status_id
    WHERE s.status_name = 'completed'
    GROUP BY
        t.client_id,
        c.client_name,
        t.asset_id,
        a.asset_symbol,
        t.transaction_date
),
running AS (
    SELECT
        *,
        SUM(buy_qty - sell_qty) OVER (
            PARTITION BY client_id, asset_id
            ORDER BY transaction_date
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS balance_qty,
        SUM(buy_value) OVER (
            PARTITION BY client_id, asset_id
            ORDER BY transaction_date
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS total_buy_value,
        SUM(buy_qty) OVER (
            PARTITION BY client_id, asset_id
            ORDER BY transaction_date
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS total_buy_qty
    FROM daily_base
)
SELECT
    r.client_id,
    r.client_name,
    r.asset_id,
    r.asset_symbol,
    r.transaction_date,
    r.buy_qty,
    r.sell_qty,
    r.balance_qty,
    r.total_buy_value / NULLIF(r.total_buy_qty, 0) AS avg_buy_price_eur,
    r.balance_qty * (r.total_buy_value / NULLIF(r.total_buy_qty, 0)) AS book_value_eur,
    mp.price_eur AS market_price_eur,
    r.balance_qty * mp.price_eur AS market_value_eur,
    (r.balance_qty * mp.price_eur)
    - (r.balance_qty * (r.total_buy_value / NULLIF(r.total_buy_qty, 0))) AS unrealized_profit_eur
FROM running r
JOIN v_daily_last_market_prices mp
    ON mp.asset_id = r.asset_id
   AND mp.price_day = r.transaction_date;