# Import von Datum und Zeit
from datetime import datetime

# Import der Hauptfunktionen aus verschiedenen Modulen
from etl.current.update_market_prices import update_market_prices
from etl.shared.generate_transactions import generate_transactions
from etl.shared.build_portfolio_snapshot import main as build_snapshot

# Hilfsfunktionen für Ausgabe und Logging
from utils.formatter import print_header
from utils.logger import get_logger


# Hauptfunktion für den aktuellen Pipeline-Prozess
def run_current_pipeline():
    # Logger erstellen
    logger = get_logger("current_pipeline")

    # Heutiges Datum holen
    today = datetime.today().strftime("%Y-%m-%d")

    try:
        # Startmeldung
        logger.info("Starting current pipeline")
        print_header("CURRENT PIPELINE START")

        # Schritt 1: Marktpreise aktualisieren
        update_market_prices()
        logger.info("Current market prices updated successfully")

        # Schritt 2: Transaktionen generieren
        generate_transactions(today, today, use_random=False)
        logger.info("Transactions for today generated successfully")

        # Schritt 3: Portfolio-Snapshot erstellen
        build_snapshot()
        logger.info("Portfolio snapshot updated successfully")

        # Endmeldung
        print_header("CURRENT PIPELINE FINISHED")
        logger.info("Finished current pipeline")

    except Exception as e:
        # Fehlerbehandlung
        logger.exception(f"Current pipeline failed: {e}")
        raise


# Startpunkt des Programms
if __name__ == "__main__":
    run_current_pipeline()


 #Diese Datei startet den gesamten Prozess.
# Die Daten werden aktualisiert,
# Transaktionen werden erstellt,  und am Ende wird ein Snapshot gebaut.
# Ich habe Logging verwendet, damit man den Prozess besser überwachen kann.