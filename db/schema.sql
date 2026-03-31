DROP DATABASE crypto_portfolio_db;
CREATE DATABASE IF NOT EXISTS crypto_portfolio_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE crypto_portfolio_db;

-- 1. countries
CREATE TABLE countries (
    country_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    country VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 2. abo_types
CREATE TABLE abo_types (
    abo_type_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    abo_type_name VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 3. asset_types
CREATE TABLE asset_types (
    asset_type_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    asset_type_name VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 4. platforms
CREATE TABLE platforms (
    platform_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    platform_name VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 5. statuses
CREATE TABLE statuses (
    status_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    status_name VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 6. currencies
CREATE TABLE currencies (
    currency_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    currency_code VARCHAR(10) NOT NULL UNIQUE,
    currency_name VARCHAR(30) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 7. clients
CREATE TABLE clients (
    client_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    client_name VARCHAR(50) NOT NULL,
    country_id INT UNSIGNED NOT NULL,
    abo_type_id INT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (country_id) REFERENCES countries(country_id),
    FOREIGN KEY (abo_type_id) REFERENCES abo_types(abo_type_id)
);

-- 8. assets
CREATE TABLE assets (
    asset_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    asset_name VARCHAR(50) NOT NULL,
    asset_symbol VARCHAR(20) NOT NULL UNIQUE,
    asset_type_id INT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (asset_type_id) REFERENCES asset_types(asset_type_id)
);

-- 9. exchange_rates
CREATE TABLE exchange_rates (
    rate_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    rate_date DATE NOT NULL,
    from_currency_id INT UNSIGNED NOT NULL,
    to_currency_id INT UNSIGNED NOT NULL,
    rate_value DECIMAL(18,8) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (from_currency_id) REFERENCES currencies(currency_id),
    FOREIGN KEY (to_currency_id) REFERENCES currencies(currency_id),
    UNIQUE (rate_date, from_currency_id, to_currency_id)
);

-- 10. transactions
CREATE TABLE transactions (
    transaction_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    client_id INT UNSIGNED NOT NULL,
    platform_id INT UNSIGNED NOT NULL,
    asset_id INT UNSIGNED NOT NULL,
    status_id INT UNSIGNED NOT NULL,
    transaction_date DATE NOT NULL,
    amount DECIMAL(18,8) NOT NULL,
    buy_price DECIMAL(18,8) NOT NULL,
    currency_id INT UNSIGNED NOT NULL,
    buy_price_eur DECIMAL(18,8) NOT NULL,
    exchange_fee_eur DECIMAL(18,8) NOT NULL DEFAULT 0.00000000,
    service_fee_eur DECIMAL(18,8) NOT NULL DEFAULT 0.00000000,
    referral_bonus_eur DECIMAL(18,8) NOT NULL DEFAULT 0.00000000,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(client_id),
    FOREIGN KEY (platform_id) REFERENCES platforms(platform_id),
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id),
    FOREIGN KEY (status_id) REFERENCES statuses(status_id),
    FOREIGN KEY (currency_id) REFERENCES currencies(currency_id)
);

-- transactions
CREATE INDEX idx_transactions_client_id ON transactions(client_id);
CREATE INDEX idx_transactions_platform_id ON transactions(platform_id);
CREATE INDEX idx_transactions_asset_id ON transactions(asset_id);
CREATE INDEX idx_transactions_status_id ON transactions(status_id);
CREATE INDEX idx_transactions_currency_id ON transactions(currency_id);
CREATE INDEX idx_transactions_transaction_date ON transactions(transaction_date);

-- exchange_rates
CREATE INDEX idx_exchange_rates_from_currency_id ON exchange_rates(from_currency_id);
CREATE INDEX idx_exchange_rates_to_currency_id ON exchange_rates(to_currency_id);
CREATE INDEX idx_exchange_rates_rate_date ON exchange_rates(rate_date);


-- API ціна активі
-- Die Tabelle market_prices speichert historische Marktpreise der Assets in EUR.“
CREATE TABLE market_prices (
    price_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    asset_id INT UNSIGNED NOT NULL,
    price_date DATETIME NOT NULL,
    price_eur DECIMAL(18,8) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id)
);

-- Щоб не було дублікатів на той самий час
CREATE UNIQUE INDEX idx_market_prices_asset_date
ON market_prices(asset_id, price_date);


SELECT * FROM market_prices;
