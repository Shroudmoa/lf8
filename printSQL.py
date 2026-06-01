##### SQL-Abfrage ausführen und ausgeben 1.2#####

import mariadb
import sys

# Verbindung zur Datenbank
try:
    db = mariadb.connect(
        host=""10.145.240.127,#100.125.20.61 #root|vm
        user="root",
        password="123",
        database="Heiner_IT"
    )
except mariadb.Error as e:
    print(f"Fehler: {e}")
    sys.exit(1) # das Progeramm schloeßenn wenn DB-Verbindung fehlschläft

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
        ##############################################################
        # Hole die Spaltennamen aus den Metadaten
        column_names = [desc[0] for desc in cursor.description]
        
        # Gebe Spaltenköpfe aus
        print("\n" + "="*100) # es wird versucht Tabellenkopf zu haben
        print(" | ".join(f"{col:20}" for col in column_names)) #20 char für jede Spalte
        print("="*100)
        
        # Gebe alle Zeilen aus
        for row in cursor.fetchall():#fetchall liefert alle zeilen zurück
            print(" | ".join(f"{str(val):20}" for val in row))
        
        print("="*100 + "\n")
        cursor.close()  # Schließe den Cursor
        ############################################################
        # weil die Tabelle riesig ist, sieht es am Ende immer noch bisschen unorganisiert aus aber es funktioniert und man kann es ja anpassen damit es sauberer aussieht 
    except mariadb.Error as e:
        print(f"Fehler bei der Abfrage: {e}")

# Aufruf der Methode
testprint(db, sql_Anweisung)
