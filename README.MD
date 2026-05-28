═══════════════════════════════════════════════════════════════════════════
            11IT2B - Könermann - Abutalebi - Gozashti
                         LF8 Projekt DOKU
═══════════════════════════════════════════════════════════════════════════



Als Übersicht:
Projekt: Verwaltung und Export der Datenbank in verschiedene Formate
Ziel: Bereitstellung von Daten in XML, CSV und HTML für verschiedene Abteilungen (Read Write Regeln + Bonus => KundenVerwaltung Web-GUI)


# MEILENSTEIN-ÜBERSICHT UND ZEITAUFWAND


┌─────────┬────────────────────────────────────────────┬──────────┬──────────┐
│ Nummer  │ Meilenstein                                │ Geplant  │ Actual   │
├─────────┼────────────────────────────────────────────┼──────────┼──────────┤
│ 1.0     │ Quellcode-Dokumentation                    │ 2h       │ 2h       │
├─────────┼────────────────────────────────────────────┼──────────┼──────────┤
│ 1.1     │ Datenbankverbindung mit MariaDB            │ 2h       │ 0,5h     │
├─────────┼────────────────────────────────────────────┼──────────┼──────────┤
│ 1.2     │ SQL-Abfrage mit Print-Ausgabe              │ 1h       │ 0,5h     │
├─────────┼────────────────────────────────────────────┼──────────┼──────────┤
│ 1.3     │ CSV-Export aus Datenbank                   │ 2h       │ 1h       │
├─────────┼────────────────────────────────────────────┼──────────┼──────────┤
│ 1.4     │ GUI mit Tkinter (Tabellendarstellung)      │ 2h       │ 2h       │
├─────────┼────────────────────────────────────────────┼──────────┼──────────┤
│ 1.5     │ CSV zu XML Konvertierung                   │ 1h       │ 0,5h     │
├─────────┼────────────────────────────────────────────┼──────────┼──────────┤
│ 1.6     │ Erweiterung: XML zu HTML                   │ 1h       │ 1h       │
├─────────┼────────────────────────────────────────────┼──────────┼──────────┤
│ 1.7     │ Dokumentation                              │ 1h       │ 0,5h     │
├─────────┼────────────────────────────────────────────┼──────────┼──────────┤
│ GESAMT  │                                            │ 12h      │ 6h       │
└─────────┴────────────────────────────────────────────┴──────────┴──────────┘


┌─────────┬────────────────────────────────────────────┬──────────┬──────────┐
│ Nummer  │ Meilenstein                                │ Geplant  │ Actual   │
├─────────┼────────────────────────────────────────────┼──────────┼──────────┤
│ 2.1     │ Dropdown-Mitarbeiterauswahl-Passwort       │ 2h       │ 1h       │
├─────────┼────────────────────────────────────────────┼──────────┼──────────┤
│ 2.2     │ Verfügbarkeit der Tools                    │ 2h       │ 1h       │
├─────────┼────────────────────────────────────────────┼──────────┼──────────┤
│ 2.3     │ Überraschung-Funktionalität(Verwaltung GUI)│ 2h       │ 3h       │
├─────────┼────────────────────────────────────────────┼──────────┼──────────┤
│ GESAMT  │                                            │ 6h       │ 5h       │
└─────────┴────────────────────────────────────────────┴──────────┴──────────┘


# AUFGETRETENE PROBLEME UND LÖSUNGEN



1. Verbindung der DB (1.1)
   ─────────────────────────
   Hürde: Server-IP und Passwort korrekt eingeben
   Lösung: Überprüfung der Credentials (100.125.20.61, root, vm, Heiner_IT)

2. SPALTENNAMEN (1.2)
   ──────────────────────────────────
   Problem: Spaltenköpfe nicht dynamisch ausgelesen
   Hürde: cursor.description verwenden für Metadaten
   Lösung: [desc[0] for desc in cursor.description]
   

3. CSV Trennzeichen (1.3)
   ──────────────────────
   Problem: CSV-Datei mit Kommas statt Semikolo
   Hurde: Deutsche Excel-Kompatibilität erfordert Semikolon
   Lösung: delimiter=';' in csv.writer() (https://docs.python.org/3/library/csv.html)
   

4. tkinterr GUI (1.4)
   ────────────────────────
   Problem: Scrollbar nicht funktionierend
   hürde: Korrekte Platzierung und Konfiguration
   lösung: Scrollbar mit tree.configure(yscroll=scrollbar.set) verbinden
   

5. XML formatierung (1.5)
   ──────────────────────
   Problem: XML nicht korrekt eingerückt (pretty print)
   Hürde: minidom.parseString() nutzen für Formatierung
   Lösung: XML mit toprettyxml(indent="  ") formatieren
   

6. HTML (1.6)
   ───────────────────────
   problem: HTML-Tabelle nicht ansehnlich
   Hürde: CSS-Styling hinzufügen
   Lösung: Inline-CSS mit Hover-Effekten und Zebra-Stripes
   

# VERWENDETE BIBLIOTHEKEN:


• mariadb: Datenbankverbindung und -abfragen
• csv: CSV-Export und -Verarbeitung
• xml.etree.ElementTree: XML-Verarbeitung
• xml.dom.minidom: XML-Formatierung (Pretty Print)
• tkinter: Grafische Benutzeroberfläche
• sys: Systemfunktionen (Fehlerbehandlung)
• flask: Web-GUI für 2.3
• datetime: Datums- und Zeitfunktionen
• hashlib: Passwort-Hashing und Sicherheitsfunktionen

# SERVER-KONFIGURATION als DOKU:


Host: 100.125.20.61
User: root
Passwort: vm
Datenbank: Heiner_IT
Typ: MariaDB

# DATEIEN UND OUTPUTS ALS DOKU 


Generierte Dateien:
  01_ConnectionTest.py - Verbindungstest 1.1
  printSQL.py - SQL-Ausgabe 1.2
  CSVExport.py - CSV-Export 1.3
  GUITabelle.py - Tkinter GUI 1.4
  CSVtoXML.py - CSV zu XML Konvertierung 1.5
  XMLtoHTML.py - XML zu HTML Konvertierung 1.6

