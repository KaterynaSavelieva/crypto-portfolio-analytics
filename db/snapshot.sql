USE crypto_portfolio_db;
DROP VIEW IF EXISTS v_portfolio_daily_snapshot;
DROP VIEW IF EXISTS v_daily_market_prices_for_snapshot;
DROP VIEW IF EXISTS v_transactions_for_snapshot;
DROP TABLE IF EXISTS portfolio_daily_snapshot;


CREATE TABLE portfolio_daily_snapshot (
    snapshot_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    snapshot_date DATE NOT NULL,
    client_id INT UNSIGNED NOT NULL,
    asset_id INT UNSIGNED NOT NULL,

    buy_qty_day DECIMAL(18,8) DEFAULT 0,
    sell_qty_day DECIMAL(18,8) DEFAULT 0,
    balance_qty DECIMAL(18,8) DEFAULT 0,

    avg_buy_price_eur DECIMAL(18,8) DEFAULT 0,
    book_value_eur DECIMAL(18,8) DEFAULT 0,

    market_price_eur DECIMAL(18,8) DEFAULT 0,
    market_value_eur DECIMAL(18,8) DEFAULT 0,

    realized_profit_day_eur DECIMAL(18,8) DEFAULT 0,
    unrealized_profit_eur DECIMAL(18,8) DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_snapshot_client
        FOREIGN KEY (client_id) REFERENCES clients(client_id),

    CONSTRAINT fk_snapshot_asset
        FOREIGN KEY (asset_id) REFERENCES assets(asset_id),

    CONSTRAINT uq_snapshot_day
        UNIQUE (snapshot_date, client_id, asset_id)
);

CREATE OR REPLACE VIEW v_transactions_for_snapshot AS
SELECT
    t.transaction_id,
    t.transaction_date,
    t.client_id,
    t.asset_id,
    t.transaction_type,
    t.amount,
    t.buy_price_eur AS price_eur
FROM transactions t
JOIN statuses s
    ON t.status_id = s.status_id
WHERE s.status_name = 'completed';

CREATE OR REPLACE VIEW v_daily_market_prices_for_snapshot AS
SELECT
    DATE(mp.price_date) AS snapshot_date,
    mp.asset_id,
    mp.price_eur AS market_price_eur
FROM market_prices mp
JOIN (
    SELECT
        asset_id,
        DATE(price_date) AS snapshot_date,
        MAX(price_date) AS last_price_datetime
    FROM market_prices
    GROUP BY
        asset_id,
        DATE(price_date)
) latest
    ON mp.asset_id = latest.asset_id
   AND DATE(mp.price_date) = latest.snapshot_date
   AND mp.price_date = latest.last_price_datetime;

CREATE OR REPLACE VIEW v_portfolio_daily_snapshot AS
SELECT
    s.snapshot_date,
    s.client_id,
    c.client_name,
    s.asset_id,
    a.asset_symbol,
    s.buy_qty_day,
    s.sell_qty_day,
    s.balance_qty,
    s.avg_buy_price_eur,
    s.book_value_eur,
    s.market_price_eur,
    s.market_value_eur,
    s.realized_profit_day_eur,
    s.unrealized_profit_eur
FROM portfolio_daily_snapshot s
JOIN clients c ON s.client_id = c.client_id
JOIN assets a ON s.asset_id = a.asset_id;
