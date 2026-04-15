# 📊 Crypto Portfolio Analytics System

## 📌 About the project

This project is a simple **data analytics system for cryptocurrencies**.  
It automatically loads market data from external APIs, processes it, and prepares it for analysis and visualization.

The goal is to analyze a crypto portfolio and calculate key metrics such as:
- profit
- loss
- portfolio value

---

## 🎯 Project goals

- Analyze cryptocurrencies (Bitcoin, Ethereum)
- Work with real API data
- Build an ETL process (Extract, Transform, Load)
- Calculate portfolio metrics
- Visualize data in Power BI

---

## 🌐 Data sources (APIs)

- **CoinGecko API** → cryptocurrency prices  
- **Exchange Rate API** → USD → EUR conversion  

Data is fetched and processed regularly.

---

## 🛠️ Technologies used

- Python → ETL pipeline and data processing  
- Pandas → data transformation  
- MySQL → database  
- Power BI → visualization  
- Jupyter Notebook → analysis and testing  
- DBeaver → database management  
- Requests → API calls  
- Windows Task Scheduler → automation  

---

## 🧱 System architecture

The system is based on a simple ETL process:

### Extract
- Load BTC and ETH market data
- Load exchange rates

### Transform
- Convert USD → EUR
- Calculate metrics
- Process transactions

### Load
- Store data in MySQL
- Create portfolio snapshots

---

## 🔄 Pipeline

Main script:

```bash
python run_current_pipeline.py
```

### Steps:
- Load market prices  
- Load exchange rates  
- Calculate data  
- Generate transactions  
- Create portfolio snapshot  
- Save data to database  

---

## 🗄️ Database

### Main tables:
- `market_prices` → BTC and ETH prices  
- `transactions` → buy/sell operations  
- `portfolio_daily_snapshot` → final analytics data  

Additional SQL views are used for easier analysis.

---

## 📊 Power BI Dashboard

The dashboard includes:

- Portfolio Value  
- BTC / ETH price trends  
- Unrealized Profit  
- Analysis per customer  

Data is loaded directly from the database.

---

## 📈 Key metrics

- **Balance Quantity** → current holdings  
- **Average Buy Price** → average purchase price  
- **Book Value** → investment value  
- **Market Value** → current value  
- **Realized Profit** → profit from sales  
- **Unrealized Profit** → potential profit  

---

## ▶️ How to run the project

### 1. Start database
Run MySQL server

### 2. Activate Python environment

### 3. Run pipeline
```bash
python run_current_pipeline.py
```

## ⏱️ Automation

The system supports automation using:

- Windows Task Scheduler  
- Regular data updates (e.g. every 2 hours)  

---

## 🧠 What this project demonstrates

This project shows a full data workflow:

- API data collection  
- ETL processing  
- SQL storage  
- Power BI visualization  

The system is simple but scalable and realistic.

---

## 👩‍💻 Author

**Kateryna Savelieva**  
Python | SQL | Data Analytics | ETL | Power BI
