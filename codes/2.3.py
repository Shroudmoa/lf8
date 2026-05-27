##### ERWEITERUNG: Datenbankstatistiken und Kundenmanagement #####

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mariadb
import sys
from datetime import datetime

# ============================================================================
# DATENBANKVERBINDUNG
# ============================================================================

try:
    db = mariadb.connect(
        host="192.168.0.79",
        user="moa",
        password="vm",
        database="Heiner_IT"
    )
except mariadb.Error as e:
    print(f"Fehler: {e}")
    sys.exit(1)

# ============================================================================
# STATISTIK-FUNKTIONEN
# ============================================================================

class DatenbankStatistik:
    """
    Klasse zur Abfrage von Datenbankstatistiken
    Zeigt Übersichtsdaten über Kunden, Bestellungen, Artikel, etc.
    """
    
    @staticmethod
    def get_kundenanzahl():
        """Zählt die Gesamtanzahl der Kunden"""
        try:
            cursor = db.cursor()
            cursor.execute("SELECT COUNT(*) FROM kunde")
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result else 0
        except mariadb.Error:
            return 0
    
    @staticmethod
    def get_bestellungsanzahl():
        """Zählt die Gesamtanzahl der Bestellungen"""
        try:
            cursor = db.cursor()
            cursor.execute("SELECT COUNT(*) FROM bestellung")
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result else 0
        except mariadb.Error:
            return 0
    
    @staticmethod
    def get_artikel_gesamtwert():
        """Berechnet den Gesamtwert aller Artikel im Lager"""
        try:
            cursor = db.cursor()
            # Summe aller Artikel (Anzahl * Preis)
            cursor.execute("""
                SELECT SUM(artikel.lagerbestand * artikel.preis) 
                FROM artikel
            """)
            result = cursor.fetchone()
            cursor.close()
            return float(result[0]) if result and result[0] else 0.0
        except mariadb.Error:
            return 0.0
    
    @staticmethod
    def get_lieferanten_count():
        """Zählt die Anzahl der Lieferanten"""
        try:
            cursor = db.cursor()
            cursor.execute("SELECT COUNT(*) FROM lieferant")
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result else 0
        except mariadb.Error:
            return 0
    
    @staticmethod
    def get_top_artikel(limit=5):
        """
        Holt die Top-Artikel mit höchstem Lagerbestand
        
        Parameter:
            limit: Anzahl der anzuzeigenden Artikel
        
        Rückgabe:
            Liste mit (Name, Lagerbestand) Tupeln
        """
        try:
            cursor = db.cursor()
            cursor.execute(f"""
                SELECT artikel_name, lagerbestand 
                FROM artikel 
                ORDER BY lagerbestand DESC 
                LIMIT {limit}
            """)
            results = cursor.fetchall()
            cursor.close()
            return results
        except mariadb.Error:
            return []
    
    @staticmethod
    def get_kategorien_statistik():
        """
        Zeigt Statistiken pro Kategorie
        
        Rückgabe:
            Liste mit (Kategorie, Anzahl Artikel, Gesamtwert)
        """
        try:
            cursor = db.cursor()
            cursor.execute("""
                SELECT 
                    kategorie.kategorie_name,
                    COUNT(artikel.artikel_id) as artikel_count,
                    SUM(artikel.lagerbestand * artikel.preis) as kategorie_wert
                FROM kategorie
                LEFT JOIN artikel ON kategorie.kategorie_id = artikel.kategorie_id
                GROUP BY kategorie.kategorie_id, kategorie.kategorie_name
            """)
            results = cursor.fetchall()
            cursor.close()
            return results
        except mariadb.Error:
            return []

# ============================================================================
# GUI FÜR STATISTIKEN
# ============================================================================

class StatistikWindow:
    """
    Grafisches Fenster zur Anzeige von Datenbankstatistiken
    Zeigt KPIs und Übersichtsdaten in einer ansprechenden Weise
    """
    
    def __init__(self, root):
        """Initialisiert das Statistik-Fenster"""
        self.root = root
        self.root.title("Heiner IT-Systems - Datenbankstatistiken")
        self.root.geometry("900x700")
        self.center_window()
        self.create_widgets()
    
    def center_window(self):
        """Zentriert das Fenster"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Erstellt alle GUI-Elemente"""
        
        # Header
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        header_frame.pack(fill="x")
        
        title_label = tk.Label(
            header_frame,
            text="📊 Datenbankstatistiken",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#2c3e50"
        )
        title_label.pack(pady=15)
        
        timestamp_label = tk.Label(
            header_frame,
            text=f"Stand: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}",
            font=("Arial", 9),
            fg="#ecf0f1",
            bg="#2c3e50"
        )
        timestamp_label.pack()
        
        # Hauptbereich mit Notebook (Tabs)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 1: Übersicht
        tab_overview = tk.Frame(notebook)
        notebook.add(tab_overview, text="Übersicht")
        self.create_overview_tab(tab_overview)
        
        # Tab 2: Top Artikel
        tab_artikel = tk.Frame(notebook)
        notebook.add(tab_artikel, text="Top Artikel")
        self.create_artikel_tab(tab_artikel)
        
        # Tab 3: Kategorien
        tab_kategorien = tk.Frame(notebook)
        notebook.add(tab_kategorien, text="Kategorien")
        self.create_kategorien_tab(tab_kategorien)
        
        # Refresh-Button
        refresh_button = tk.Button(
            self.root,
            text="🔄 Aktualisieren",
            command=self.refresh_data,
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        )
        refresh_button.pack(pady=10)
    
    def create_overview_tab(self, parent):
        """Erstellt die Übersichts-Tab"""
        
        # Statistik-Daten laden
        kundenanzahl = DatenbankStatistik.get_kundenanzahl()
        bestellungsanzahl = DatenbankStatistik.get_bestellungsanzahl()
        artikel_wert = DatenbankStatistik.get_artikel_gesamtwert()
        lieferanten = DatenbankStatistik.get_lieferanten_count()
        
        # Statistik-Boxen
        stats_frame = tk.Frame(parent)
        stats_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Kunde-Box
        self.create_stat_box(
            stats_frame,
            "👥 Kunden",
            str(kundenanzahl),
            "Insgesamt",
            "#3498db"
        ).grid(row=0, column=0, padx=10, pady=10, sticky="nsew
        # Bestellung-Box
        self.create_stat_box(
            stats_frame,
            "📦 Bestellungen",
            str(bestellungsanzahl),
            "Insgesamt",
            "#e74c3c"
        ).grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Artikel-Wert-Box
        self.create_stat_box(
            stats_frame,
            "💰 Lagerwert",
            f"€{artikel_wert:,.2f}",
            "Gesamtwert",
            "#2ecc71"
        ).grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        
        # Lieferanten-Box
        self.create_stat_box(
            stats_frame,
            "🚚 Lieferanten",
            str(lieferanten),
            "Aktiv",
            "#f39c12"
        ).grid(row=0, column=3, padx=10, pady=10, sticky="nsew")
        
        # Grid-Gewichte für responsive Layout
        for i in range(4):
            stats_frame.grid_columnconfigure(i, weight=1)
        
        # Zusätzliche Info-Section
        info_frame = tk.Frame(parent, bg="#ecf0f1")
        info_frame.pack(fill="both", padx=20, pady=20)
        
        info_label = tk.Label(
            info_frame,
            text="📊 Schnellübersicht",
            font=("Arial", 12, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        info_label.pack(anchor="w", pady=10)
        
        durchschnitt_kunden = kundenanzahl if kundenanzahl > 0 else 0
        bestellungen_pro_kunde = round(bestellungsanzahl / durchschnitt_kunden, 2) if durchschnitt_kunden > 0 else 0
        
        info_text = f"""
        • Durchschnittliche Bestellungen pro Kunde: {bestellungen_pro_kunde}
        • Durchschnittlicher Lagerwert pro Artikel: €{artikel_wert / max(1, 100)}
        • Lieferanten-zu-Artikel-Verhältnis: {lieferanten}
        """
        
        info_display = tk.Label(
            info_frame,
            text=info_text.strip(),
            font=("Arial", 10),
            bg="#ecf0f1",
            fg="#34495e",
            justify="left"
        )
        info_display.pack(anchor="w", pady=10)
    
    def create_artikel_tab(self, parent):
        """Erstellt die Top-Artikel-Tab"""
        
        # Treeview-Frame
        tree_frame = tk.Frame(parent)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Treeview mit Spalten
        columns = ("Artikel", "Lagerbestand")
        tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            height=15,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=tree.yview)
        
        # Column Headings
        tree.heading("#0", text="Rang")
        tree.heading("Artikel", text="Artikelname")
        tree.heading("Lagerbestand", text="Lagerbestand")
        
        # Column Widths
        tree.column("#0", width=50)
        tree.column("Artikel", width=300)
        tree.column("Lagerbestand", width=150)
        
        # Daten laden
        top_artikel = DatenbankStatistik.get_top_artikel(10)
        
        for index, (artikel_name, lagerbestand) in enumerate(top_artikel, 1):
            tree.insert("", "end", text=str(index), values=(artikel_name, lagerbestand))
        
        tree.pack(fill="both", expand=True)
        
        # Info-Label
        info_label = tk.Label(
            parent,
            text=f"Zeigt die Top 10 Artikel mit dem höchsten Lagerbestand",
            font=("Arial", 9),
            fg="#7f8c8d",
            bg=parent.cget("bg")
        )
        info_label.pack(pady=5)
    
    def create_kategorien_tab(self, parent):
        """Erstellt die Kategorien-Statistik-Tab"""
        
        # Treeview-Frame
        tree_frame = tk.Frame(parent)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Treeview mit Spalten
        columns = ("Artikel_Count", "Gesamtwert")
        tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            height=15,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=tree.yview)
        
        # Column Headings
        tree.heading("#0", text="Kategorie")
        tree.heading("Artikel_Count", text="Anzahl Artikel")
        tree.heading("Gesamtwert", text="Gesamtwert")
        
        # Column Widths
        tree.column("#0", width=150)
        tree.column("Artikel_Count", width=150)
        tree.column("Gesamtwert", width=150)
        
        # Daten laden
        kategorien = DatenbankStatistik.get_kategorien_statistik()
        
        for kategorie_name, artikel_count, kategorie_wert in kategorien:
            wert_str = f"€{float(kategorie_wert or 0):,.2f}"
            tree.insert("", "end", text=kategorie_name or "Keine", 
                       values=(artikel_count or 0, wert_str))
        
        tree.pack(fill="both", expand=True)
        
        # Info-Label
        info_label = tk.Label(
            parent,
            text=f"Kategorienanalyse mit Artikel-Anzahl und Lagerwert pro Kategorie",
            font=("Arial", 9),
            fg="#7f8c8d",
            bg=parent.cget("bg")
        )
        info_label.pack(pady=5)
    
    def create_stat_box(self, parent, title, value, subtitle, color):
        """
        Erstellt eine Statistik-Box mit Titel, Wert und Farbe
        
        Parameter:
            parent: Parent-Widget
            title: Titel der Box
            value: Anzuzeigende Zahl/Wert
            subtitle: Untertitel
            color: Hintergrundfarbe
        
        Rückgabe:
            Frame mit der erstellten Box
        """
        box = tk.Frame(parent, bg=color, relief="flat")
        box.config(height=120)
        
        # Titel
        title_label = tk.Label(
            box,
            text=title,
            font=("Arial", 11, "bold"),
            fg="white",
            bg=color
        )
        title_label.pack(pady=(10, 5))
        
        # Wert (groß)
        value_label = tk.Label(
            box,
            text=value,
            font=("Arial", 24, "bold"),
            fg="white",
            bg=color
        )
        value_label.pack(pady=5)
        
        # Untertitel
        subtitle_label = tk.Label(
            box,
            text=subtitle,
            font=("Arial", 9),
            fg="rgba(255,255,255,0.8)",
            bg=color
        )
        subtitle_label.pack(pady=(5, 10))
        
        return box
    
    def refresh_data(self):
        """Aktualisiert alle Daten - löscht und erstellt alle Widgets neu"""
        # Alle Widgets löschen
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Notebook):
                widget.destroy()
        
        # Neue Widgets erstellen
        self.create_widgets()
        messagebox.showinfo(
            "Erfolg",
            "Datenbankstatistiken erfolgreich aktualisiert!"
        )

# ============================================================================
# KUNDENMANAGEMENT-FUNKTIONEN
# ============================================================================

class KundenManager:
    """
    Klasse zur Verwaltung von Kundendaten
    Ermöglicht: Hinzufügen, Löschen, Bearbeiten, Suchen von Kunden
    """
    
    @staticmethod
    def add_kunde(vorname, nachname, email, telefon, adresse):
        """
        Fügt einen neuen Kunden zur Datenbank hinzu
        
        Parameter:
            vorname: Vorname des Kunden
            nachname: Nachname des Kunden
            email: E-Mail-Adresse
            telefon: Telefonnummer
            adresse: Adresse
        
        Rückgabe:
            True bei Erfolg, False bei Fehler
        """
        try:
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO kunde (vorname, nachname, email, telefon, adresse)
                VALUES (?, ?, ?, ?, ?)
            """, (vorname, nachname, email, telefon, adresse))
            db.commit()
            cursor.close()
            return True
        except mariadb.Error as e:
            print(f"Fehler beim Hinzufügen des Kunden: {e}")
            return False
    
    @staticmethod
    def delete_kunde(kunde_id):
        """
        Löscht einen Kunden aus der Datenbank
        
        Parameter:
            kunde_id: ID des zu löschenden Kunden
        
        Rückgabe:
            True bei Erfolg, False bei Fehler
        """
        try:
            cursor = db.cursor()
            cursor.execute("DELETE FROM kunde WHERE kunde_id = ?", (kunde_id,))
            db.commit()
            cursor.close()
            return True
        except mariadb.Error as e:
            print(f"Fehler beim Löschen des Kunden: {e}")
            return False
    
    @staticmethod
    def update_kunde(kunde_id, vorname=None, nachname=None, email=None, telefon=None, adresse=None):
        """
        Aktualisiert die Daten eines Kunden
        
        Parameter:
            kunde_id: ID des Kunden
            Weitere Parameter: Zu aktualisierende Felder (optional)
        
        Rückgabe:
            True bei Erfolg, False bei Fehler
        """
        try:
            cursor = db.cursor()
            updates = []
            params = []
            
            if vorname:
                updates.append("vorname = ?")
                params.append(vorname)
            if nachname:
                updates.append("nachname = ?")
                params.append(nachname)
            if email:
                updates.append("email = ?")
                params.append(email)
            if telefon:
                updates.append("telefon = ?")
                params.append(telefon)
            if adresse:
                updates.append("adresse = ?")
                params.append(adresse)
            
            if not updates:
                return False
            
            params.append(kunde_id)
            query = f"UPDATE kunde SET {', '.join(updates)} WHERE kunde_id = ?"
            cursor.execute(query, params)
            db.commit()
            cursor.close()
            return True
        except mariadb.Error as e:
            print(f"Fehler beim Aktualisieren des Kunden: {e}")
            return False
    
    @staticmethod
    def get_all_kunden():
        """
        Holt alle Kunden aus der Datenbank
        
        Rückgabe:
            Liste mit Kunden-Tupeln
        """
        try:
            cursor = db.cursor()
            cursor.execute("""
                SELECT kunde_id, vorname, nachname, email, telefon, adresse 
                FROM kunde
                ORDER BY nachname, vorname
            """)
            results = cursor.fetchall()
            cursor.close()
            return results
        except mariadb.Error:
            return []
    
    @staticmethod
    def search_kunde(search_term):
        """
        Sucht Kunden nach Namen oder E-Mail
        
        Parameter:
            search_term: Suchbegriff
        
        Rückgabe:
            Liste mit gefundenen Kunden-Tupeln
        """
        try:
            cursor = db.cursor()
            cursor.execute("""
                SELECT kunde_id, vorname, nachname, email, telefon, adresse 
                FROM kunde
                WHERE vorname LIKE ? OR nachname LIKE ? OR email LIKE ?
                ORDER BY nachname, vorname
            """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
            results = cursor.fetchall()
            cursor.close()
            return results
        except mariadb.Error:
            return []

# ============================================================================
# GUI FÜR KUNDENMANAGEMENT
# ============================================================================

class KundenWindow:
    """
    GUI-Fenster für Kundenmanagement
    Zeigt Liste, erlaubt Suche, Hinzufügen, Bearbeiten, Löschen
    """
    
    def __init__(self, root):
        """Initialisiert das Kunden-Fenster"""
        self.root = root
        self.root.title("Heiner IT-Systems - Kundenmanagement")
        self.root.geometry("1000x600")
        self.center_window()
        self.selected_kunde = None
        self.create_widgets()
        self.load_kunden()
    
    def center_window(self):
        """Zentriert das Fenster"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Erstellt alle GUI-Elemente"""
        
        # Header
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        header_frame.pack(fill="x")
        
        title_label = tk.Label(
            header_frame,
            text="👥 Kundenmanagement",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#2c3e50"
        )
        title_label.pack(pady=15)
        
        # Toolbar mit Suchfeld
        toolbar_frame = tk.Frame(self.root, bg="#ecf0f1")
        toolbar_frame.pack(fill="x", padx=10, pady=10)
        
        search_label = tk.Label(
            toolbar_frame,
            text="Suche:",
            font=("Arial", 10),
            bg="#ecf0f1"
        )
        search_label.pack(side="left", padx=5)
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search_changed)
        search_entry = tk.Entry(
            toolbar_frame,
            textvariable=self.search_var,
            width=30,
            font=("Arial", 10)
        )
        search_entry.pack(side="left", padx=5)
        
        # Button-Frame
        button_frame = tk.Frame(toolbar_frame, bg="#ecf0f1")
        button_frame.pack(side="right")
        
        add_button = tk.Button(
            button_frame,
            text="➕ Neu",
            command=self.open_add_window,
            bg="#27ae60",
            fg="white",
            font=("Arial", 9),
            padx=10
        )
        add_button.pack(side="left", padx=5)
        
        edit_button = tk.Button(
            button_frame,
            text="✏️
