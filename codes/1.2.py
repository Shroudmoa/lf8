##### SQL-Abfrage ausführen und ausgeben #####

import mariadb
import sys

# Verbindung zur Datenbank
try:
    db = mariadb.connect(
        host="100.125.20.61",
        user="root",
        password="vm",
        database="Heiner_IT"
    )
except mariadb.Error as e:
    print(f"Fehler: {e}")
    sys.exit(1)

# SQL-Anweisung zum Abrufen aller Mitarbeiter
sql_Anweisung = "SELECT * FROM personal"  # Alle Mitarbeiter aus der personal-Tabelle

# Gibt nach erfolgreicher Verbindung mit der Datenbank die SQL-Abfrage aus
def testprint(dbc, sql_Anweisung_str):
    """
    Führt eine SQL-Abfrage aus und gibt die Ergebnisse formatiert aus
    
    Parameter:
        dbc: Datenbankverbindungsobjekt
        sql_Anweisung_str: Die auszuführende SQL-Anweisung
    """
    try:
        cursor = dbc.cursor()  # Erstelle Cursor für SQL-Befehle
        cursor.execute(sql_Anweisung_str)  # Führe SQL-Befehl aus
        
        # Hole die Spaltennamen aus den Metadaten
        column_names = [desc[0] for desc in cursor.description]
        
        # Gebe Spaltenköpfe aus
        print("\n" + "="*100)
        print(" | ".join(f"{col:20}" for col in column_names))
        print("="*100)
        
        # Gebe alle Zeilen aus
        for row in cursor.fetchall():
            print(" | ".join(f"{str(val):20}" for val in row))
        
        print("="*100 + "\n")
        cursor.close()  # Schließe den Cursor
        
    except mariadb.Error as e:
        print(f"Fehler bei der Abfrage: {e}")

# Aufruf der Methode
testprint(db, sql_Anweisung)
