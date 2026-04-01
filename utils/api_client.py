import requests
import time


# Diese Funktion sendet eine API-Anfrage mit Retry-Logik
def fetch_with_retry(url, params=None, max_retries=3):

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, params=params,timeout=10)  # Sende Anfrage an die API (maximal 10 Sekunden warten)
            response.raise_for_status()  # Prüft, ob die Antwort erfolgreich ist (z.B. Status 200)
            return response.json()  # Erfolg → Daten zurückgeben

        except requests.exceptions.Timeout:
            print(f"Request timed out... Versuch {attempt}/{max_retries}")  # Wenn die Anfrage zu lange dauert (mehr als 10 Sekunden)

        except requests.exceptions.ConnectionError:
            print(f"Connection error... Versuch {attempt}/{max_retries}")  # Wenn keine Verbindung zum Server möglich ist

        except requests.exceptions.HTTPError as e:
            print(f"HTTP error: {e}... Versuch {attempt}/{max_retries}")  # Wenn der Server einen Fehler zurückgibt (z.B. 404, 500)

        except requests.exceptions.RequestException as e:
            print(f"Unexpected  error: {e}")  # Allgemeiner Fehler (alle anderen Fehler)
            break  # andere Fehler → nicht erneut versuchen

        time.sleep(2)  # Warten vor dem nächsten Versuch
        print("Alle Versuche fehlgeschlagen")
        return None

