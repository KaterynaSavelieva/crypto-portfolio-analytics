select * from v_transactions_overview vto;
-- truncate table market_prices;

-- alter table market_prices add column price_usd decimal (18,2);
-- alter table market_prices add column eur_rate decimal(10,6);
-- alter table  market_prices add constraint uq_market_prices_asset_date unique (asset_id, price_date);
-- alter table market_prices add unique (asset_id, price_date);
-- drop table exchange_rates;
show tables;

-- alter table transactions add column transaction_type enum ('BUY', 'SELL'); 
-- update transactions t set transaction_type = 'BUY' where transaction_type is null;
-- alter table transactions modify column transaction_type ENUM('BUY', 'SELL') NOT NULL DEFAULT 'BUY';
-- truncate table transactions;

select * from clients;
select * from abo_types;
select * from platforms;
select * from transactions;

select count(*) from market_prices;
select count(*) from transactions;


select transaction_type, count(*)
from transactions
group by transaction_type;

select min(price_date), max(price_date) from market_prices;

select count(*) from market_prices where price_usd  is null;
SELECT COUNT(*) FROM market_prices WHERE price_eur IS NULL;
SELECT COUNT(*) FROM market_prices WHERE eur_rate IS NULL;

SELECT
    COUNT(*) AS total_rows,
    SUM(price_usd IS NULL) AS price_usd_nulls,
    SUM(price_eur IS NULL) AS price_eur_nulls,
    SUM(eur_rate IS NULL) AS eur_rate_nulls
FROM market_prices;


-- "Ich überprüfe, wie viele unterschiedliche Assets in den Marktdaten vorhanden sind
select count(distinct asset_id) from market_prices; -- cr
-- or
select a.asset_symbol 
from market_prices mp 
join assets a on mp.asset_id = a.asset_id 
group by a.asset_symbol;


-- DROP VIEW IF EXISTS v_transactions_overview;
SHOW FULL TABLES IN crypto_portfolio_db WHERE TABLE_TYPE = 'VIEW';
SHOW FULL TABLES IN crypto_portfolio_db WHERE TABLE_TYPE = 'VIEW';
-- DROP VIEW crypto_portfolio_db.v_transactions_overview;

SHOW PROCESSLIST;

SELECT 
	date_format(transaction_date, '%Y-%m') as month,
    platform_name,
    client_name, 
    SUM(pnl_eur) AS total_profit
FROM v_transactions_with_price
GROUP BY platform_name, client_name, date_format(transaction_date, '%Y-%m')
with rollup
-- order by client_name, platform_name, total_profit, month
;



UPDATE transactions
SET status_id = 2 -- completed
WHERE status_id = 1
AND transaction_date < CURDATE();


create or replace view v_transaction_clean as
select
    t.transaction_id,
    c.client_name,
    p.platform_name,
    a.asset_symbol,
    cur.currency_code AS currency,
    t.transaction_date,
    t.transaction_type,
    t.amount,
    t.buy_price,
    t.buy_price_eur,
    t.exchange_fee_eur,
    t.service_fee_eur,
    t.referral_bonus_eur	
from transactions t
join clients c on t.client_id=c.client_id
join platforms p on t.platform_id = p.platform_id
join assets a on t.asset_id = a.asset_id
join currencies cur on t.currency_id = cur.currency_id;

select * from v_transaction_clean;

create or replace view v_portfolio_balance_simple  as
select
	client_name,
	platform_name,
	asset_symbol,
	sum(
	case 
		when transaction_type = 'BUY' then amount
		when transaction_type = 'SELL' then -amount
		else 0
	end
	) as net_amount
from v_transaction_clean
group by
	client_name,
	platform_name,
	asset_symbol;

SELECT * FROM v_portfolio_balance_simple
ORDER BY client_name, platform_name, asset_symbol;

create or replace view v_market_prices_latest_simple as
select
	mp.asset_id,
	a.asset_symbol,
	mp.price_date,
	mp.price_eur
from market_prices mp
join assets a 
	on mp.asset_id = a.asset_id
join (
	select
		asset_id,
		max(price_date) as max_price_date
	from market_prices
	group by asset_id
) latest
	on mp.asset_id=latest.asset_id
	and mp.price_date=latest.max_price_date;

SELECT * FROM v_market_prices_latest_simple;


create or replace view v_portfolio_value_simple as
select
	b.client_name,
	b.platform_name,
	b.asset_symbol,
	b.net_amount,
	p.price_date as latest_price_date,
	p.price_eur as latest_price_eur,
	b.net_amount*p.price_eur as current_value_eur
from v_portfolio_balance_simple b
join v_market_prices_latest_simple p
	on b.asset_symbol= p.asset_symbol;

select * from v_portfolio_value_simple 
order by client_name, platform_name, asset_symbol;

select client_name,
	sum(net_amount)
from v_portfolio_value_simple 
group by client_name;


-- truncate table transactions;
select * from transactions;


