USE crypto_portfolio_db;

-- countries
INSERT INTO countries (country) VALUES
('Austria'),
('Germany'),
('Switzerland');


--  abo_types
INSERT INTO abo_types (abo_type_name) VALUES
('Free'),
('Premium');

--  asset_types
INSERT INTO asset_types (asset_type_name) VALUES
('Crypto');


--  platforms
INSERT INTO platforms (platform_name) VALUES
('Binance'),
('Coinbase'),
('Kraken');

--  statuses
INSERT INTO statuses (status_name) VALUES
('pending'),
('completed'),
('failed');

--  currencies
INSERT INTO currencies (currency_code, currency_name) VALUES
('USD', 'US Dollar'),
('EUR', 'Euro');


--  assets
INSERT INTO assets (asset_name, asset_symbol, asset_type_id) VALUES
('Bitcoin', 'BTC', 1),
('Ethereum', 'ETH', 1);

--  clients
INSERT INTO clients (client_name, country_id, abo_type_id) VALUES
('Anna', 1, 2),
('Mark', 2, 1),
('Julia', 1, 2),
('Tom', 2, 1),
('Lisa', 1, 2),
('David', 3, 1);



--  transaction
INSERT INTO transactions (
    client_id, platform_id, asset_id, status_id,
    transaction_date, amount, buy_price, currency_id,
    buy_price_eur, exchange_fee_eur, service_fee_eur, referral_bonus_eur,
    transaction_type
) VALUES
(1, 1, 1, 2, '2025-01-10', 0.05, 42000, 1, 38640, 10, 5, 0, 'BUY'),
(2, 2, 1, 2, '2025-02-15', 0.02, 45000, 1, 41850, 8, 4, 0, 'BUY'),
(3, 3, 1, 2, '2025-03-01', 0.01, 47000, 1, 42770, 7, 3, 1, 'BUY'),
(4, 1, 2, 2, '2025-03-10', 1.2, 2500, 1, 2350, 5, 2, 0, 'BUY'),
(5, 2, 2, 2, '2025-04-01', 0.8, 2600, 1, 2392, 6, 3, 2, 'BUY'),

-- SELL приклад 
(1, 1, 1, 2, '2025-04-05', 0.02, 50000, 1, 46000, 5, 2, 0, 'SELL'),

-- pending
(6, 3, 1, 1, '2025-04-06', 0.03, 48000, 1, 44160, 9, 4, 0, 'BUY');