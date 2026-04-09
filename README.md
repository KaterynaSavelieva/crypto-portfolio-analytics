📊 Crypto Portfolio Analytics System
📌 Projektbeschreibung

Dieses Projekt ist ein einfaches Data-Analytics-System für Kryptowährungen.
Es lädt automatisch Marktdaten aus externen APIs, verarbeitet diese Daten und stellt sie für Analysen und Visualisierung bereit.

Das Ziel ist es, ein Portfolio von Kryptowährungen zu analysieren und wichtige Kennzahlen wie Gewinn, Verlust und Portfolio-Wert zu berechnen.

🎯 Ziele des Projekts
    Analyse von Kryptowährungen (Bitcoin, Ethereum)
    Arbeiten mit echten Daten aus APIs
    Aufbau eines ETL-Prozesses (Extract, Transform, Load)
    Berechnung von Portfolio-Kennzahlen
    Visualisierung der Ergebnisse in Power BI

🔗 Datenquellen (APIs)
CoinGecko API → Kryptowährungspreise
Exchange Rate API → USD → EUR Wechselkurse

Die Daten werden regelmäßig geladen und verarbeitet.

⚙️ Technologien
Python → ETL-Prozess und Datenverarbeitung
Pandas → Datenanalyse und Transformation
MySQL → Datenbank
Power BI → Visualisierung
Jupyter Notebook → Analyse und Tests
DBeaver → Datenbankverwaltung
Requests → API-Zugriffe
Windows Task Scheduler → Automatisierung
🏗️ Systemarchitektur

Das System basiert auf einem einfachen ETL-Prozess:

Extract
Laden von Marktdaten (BTC, ETH)
Laden von Wechselkursen
Transform
Umrechnung USD → EUR
Berechnung von Kennzahlen
Verarbeitung von Transaktionen
Load
Speicherung in MySQL
Aufbau von Portfolio-Snapshots
🔄 Ablauf (Pipeline)

Die Hauptpipeline:

run_current_pipeline.py

Schritte:

Marktpreise laden
Wechselkurse laden
Daten berechnen
Transaktionen generieren
Portfolio-Snapshot erstellen
Daten in Datenbank speichern
🗄️ Datenbank

Wichtige Tabellen:

market_prices → Preise von BTC und ETH
transactions → Kauf- und Verkaufsdaten
portfolio_daily_snapshot → fertige Daten für Analyse

Zusätzlich wurden Views erstellt für einfachere Analyse.

📈 Power BI Dashboard

Das Dashboard zeigt:

Portfolio Value
Preisentwicklung (BTC, ETH)
Unrealized Profit
Analyse pro Kunde

Die Daten werden direkt aus der Datenbank geladen.

🧠 Wichtige Kennzahlen
Balance Quantity → aktueller Bestand
Average Buy Price → durchschnittlicher Kaufpreis
Book Value → Investitionswert
Market Value → aktueller Marktwert
Realized Profit → realisierter Gewinn
Unrealized Profit → nicht realisierter Gewinn
▶️ Projekt starten
Datenbank starten (MySQL)
Python-Umgebung aktivieren
Pipeline ausführen:
python run_current_pipeline.py
🔁 Automatisierung

Das System kann automatisch ausgeführt werden:

Windows Task Scheduler
Regelmäßige Updates der Daten (z. B. alle 2 Stunden)
📌 Fazit

Dieses Projekt zeigt, wie ein vollständiger Data-Analytics-Prozess aufgebaut werden kann:

Daten laden (API)
Daten verarbeiten (ETL)
Daten speichern (SQL)
Daten visualisieren (Power BI)

Das System ist einfach, aber skalierbar und realitätsnah.

👩‍💻 Autorin

Kateryna Savelieva
