##### Graphisches Interface mit Tkinter #####

import tkinter as tk
from tkinter import ttk
import mariadb
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

# Daten aus der Datenbank auslesen
def read_from_database(table_name):
    """
    Liest Daten aus einer Tabelle der Datenbank aus
    
    Parameter:
        table_name: Name der Tabelle
    
    Rückgabe:
        Tuple mit (Spaltennamen, Datenzeilen)
    """
    try:
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        
        # Hole Spaltennamen
        column_names = [desc[0] for desc in cursor.description]
        
        # Hole alle Daten
        rows = cursor.fetchall()
        cursor.close()
        
        return column_names, rows
    except mariadb.Error as e:
        print(f"Fehler: {e}")
        return [], []

# Tkinter-Setup
def darstellung_tabelle():
    """
    Erstellt und zeigt das Tkinter-Fenster mit einer Tabelle an
    """
    # Erstelle Hauptfenster
    root = tk.Tk()
    root.title("Heiner IT-Systems - Datenverwaltung")
    root.geometry("1000x600")
    
    # Lese Daten aus der artikel-Tabelle
    column_names, rows = read_from_database("artikel")
    
    # Erstelle Treeview (Tabelle)
    tree = ttk.Treeview(root, columns=column_names, show='headings')
    
    # Definiere Spalten
    for col in column_names:
        tree.heading(col, text=col)  # Spaltenüberschrift
        tree.column(col, width=100)  # Spaltenbreite
    
    # Füge Daten in die Tabelle ein
    for row in rows:
        tree.insert('', 'end', values=row)
    
    # Scrollbar hinzufügen
    scrollbar = ttk.Scrollbar(root, orient='vertical', command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    
    # Platziere Tabelle und Scrollbar
    tree.pack(fill='both', expand=True, padx=10, pady=10)
    scrollbar.pack(side='right', fill='y')
    
    # Starte das Fenster
    root.mainloop()

# Aufruf der GUI
darstellung_tabelle()
