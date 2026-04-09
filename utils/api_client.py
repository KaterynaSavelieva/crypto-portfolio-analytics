# Bibliotheken für HTTP-Anfragen und Zeitsteuerung
import requests
import time


# Diese Funktion sendet eine API-Anfrage mit Retry-Logik
def fetch_with_retry(url, params=None, max_retries=3):

    # Schleife für mehrere Versuche
    for attempt in range(1, max_retries + 1):
        try:
            # API-Anfrage senden
            response = requests.get(url, params=params, timeout=10)

            # Prüfen, ob die Anfrage erfolgreich war
            response.raise_for_status()

            # JSON-Daten zurückgeben
            return response.json()

        # Fehler: Timeout
        except requests.exceptions.Timeout:
            print(f"Request timed out... Versuch {attempt}/{max_retries}")

        # Fehler: Verbindungsproblem
        except requests.exceptions.ConnectionError:
            print(f"Connection error... Versuch {attempt}/{max_retries}")

        # Fehler: HTTP-Fehler (z.B. 404, 500)
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error: {e}... Versuch {attempt}/{max_retries}")

        # Andere Fehler
        except requests.exceptions.RequestException as e:
            print(f"Unexpected error: {e}")
            break

        # Warten vor dem nächsten Versuch
        time.sleep(2)

    # Wenn alle Versuche fehlschlagen
    print("Alle Versuche fehlgeschlagen")
    return None