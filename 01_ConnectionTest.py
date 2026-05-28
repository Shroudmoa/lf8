##### Verbindung zur Datenbank herstellen 1.1 #####
import mariadb
import sys

# Connect to the MySQL database 
# - Verbindung zur Datenbank mit den angegebenen Parametern herstellen
try:
    db = mariadb.connect(
        host="100.125.20.61",        # Server-IP-Adresse
        user="root",                  # Benutzer
        password="vm",               # Passwort
        database="Heiner_IT"         # Datenbankname
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Die Methode prüft ob eine erfolgreiche Verbindung zur Datenbank hergestellt werden kann.
# Ausgabe: gibt "successful" oder "failed" als print-Ausgabe zurück
def testConnection(dbc):  # dbc steht für die Datenbankverbindung die überprüft werden soll
    """
    Testet die Datenbankverbindung durch eine einfache Abfrage
    
    Parameter:
        dbc: Datenbankverbindungsobjekt
    
    Rückgabe:
        Gibt "successful" oder "failed" aus
    """
    try:
        cursor = dbc.cursor()  # Erstelle einen Cursor zur Ausführung von SQL-Befehlen
        cursor.execute("SELECT 1")  # Einfache Test-Abfrage
        result = cursor.fetchone()  # Hole das Ergebnis
        cursor.close()  # Schließe den Cursor
        
        if result:
            print("Datenbankverbindung erfolgreich!")
            return "successful"
        else:
            print("Datenbankverbindung fehlgeschlagen!")
            return "failed"
    except mariadb.Error as e:
        print(f"✗ Fehler: {e}")
        return "failed"

# Aufruf der Methode zum Testen der Datenbankverbindung
testConnection(db)
