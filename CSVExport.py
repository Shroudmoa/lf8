##### CSV-Export aus Datenbank #####

import mariadb
import csv
import sys

# Verbindung zur Datenbank
try:
    db = mariadb.connect(
        host="10.145.240.127",
        user="root",
        password="123",
        database="Heiner_IT"
    )
except mariadb.Error as e:
    print(f"Fehler: {e}")
    sys.exit(1)

# SQL-Abfrage für den Lagerbestand
sql_bestand = "SELECT * FROM artikel"  # Alle Artikel aus der artikel-Tabelle
# nicht im Einsatzt
# Funktion zum Exportieren einer Tabelle in CSV
def tabelle_to_csv(tabelle_name, dbc, output_file="export.csv"):
    """
    Exportiert eine Datenbanktabelle in eine CSV-Datei
    
    Parameter:
        tabelle_name: Name der zu exportierenden Tabelle
        dbc: Datenbankverbindungsobjekt
        output_file: Name der Ausgabedatei (Standard: export.csv)
    """
    try:
        cursor = dbc.cursor()  # Erstelle Cursor
        cursor.execute(f"SELECT * FROM {tabelle_name}")  # Wähle alle Daten aus
        
        # Hole Spaltennamen aus Metadaten
        column_names = [desc[0] for desc in cursor.description]
        
        # Hole alle Daten
        rows = cursor.fetchall()
        
        # Schreibe in CSV-Datei
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')  # Verwende Semikolon als Trennzeichen
            writer.writerow(column_names)  # Schreibe Spaltenköpfe
            writer.writerows(rows)  # Schreibe alle Datenzeilen
        
        print(f"CSV-Export erfolgreich: {output_file}")
        cursor.close()
        
    except mariadb.Error as e:
        print(f"Fehler beim CSV-Export: {e}")

# Aufruf für den Artikel-Lagerbestand
tabelle_to_csv("artikel", db, "lagerbestand.csv")
