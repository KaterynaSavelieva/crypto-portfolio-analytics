-- 
DROP DATABASE IF EXISTS crypto_portfolio_db;

CREATE DATABASE crypto_portfolio_db
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
    CONSTRAINT fk_clients_country
        FOREIGN KEY (country_id) REFERENCES countries(country_id),
    CONSTRAINT fk_clients_abo_type
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
    CONSTRAINT fk_assets_asset_type
        FOREIGN KEY (asset_type_id) REFERENCES asset_types(asset_type_id)
);

-- 9. market_prices
CREATE TABLE market_prices (
    price_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    asset_id INT UNSIGNED NOT NULL,
    price_date DATETIME NOT NULL,
    price_usd DECIMAL(18,2) DEFAULT NULL,
    eur_rate DECIMAL(10,6) DEFAULT NULL,
    price_eur DECIMAL(18,8) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_market_prices_asset
        FOREIGN KEY (asset_id) REFERENCES assets(asset_id)
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
    transaction_type ENUM('BUY','SELL') NOT NULL DEFAULT 'BUY',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_transactions_client
        FOREIGN KEY (client_id) REFERENCES clients(client_id),
    CONSTRAINT fk_transactions_platform
        FOREIGN KEY (platform_id) REFERENCES platforms(platform_id),
    CONSTRAINT fk_transactions_asset
        FOREIGN KEY (asset_id) REFERENCES assets(asset_id),
    CONSTRAINT fk_transactions_status
        FOREIGN KEY (status_id) REFERENCES statuses(status_id),
    CONSTRAINT fk_transactions_currency
        FOREIGN KEY (currency_id) REFERENCES currencies(currency_id)
);


-- INDEXES: transactions
CREATE INDEX idx_transactions_client_id ON transactions(client_id);
CREATE INDEX idx_transactions_platform_id ON transactions(platform_id);
CREATE INDEX idx_transactions_asset_id ON transactions(asset_id);
CREATE INDEX idx_transactions_status_id ON transactions(status_id);
CREATE INDEX idx_transactions_currency_id ON transactions(currency_id);
CREATE INDEX idx_transactions_transaction_date ON transactions(transaction_date);
CREATE INDEX idx_transactions_type ON transactions(transaction_type);

-- Combined index
CREATE INDEX idx_transactions_asset_date ON transactions(asset_id, transaction_date);

-- INDEXES: market_prices
CREATE INDEX idx_market_prices_asset_id ON market_prices(asset_id);
CREATE INDEX idx_market_prices_price_date ON market_prices(price_date);

-- UNIQUE: no duplicates for same asset and timestamp
CREATE UNIQUE INDEX idx_market_prices_asset_date ON market_prices(asset_id, price_date);