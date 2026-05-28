##### Hauptprogramm mit rollenbasiertem Tool-Zugriff 2.2 ##
import tkinter as tk #tikintert gui
from tkinter import ttk # bessere widgets
from tkinter import messagebox # fehlermeldung und info fenste
import subprocess# zum ausführen von anderen python datein
import sys # für sys.executable um den Pfad zum python interpreter zu bekommen 


# KONFIGURATION: Tools pro Abteilung einfach definieren (rechte geben) 
tools_pro_abteilung = {
    "Lager": {
        "print_SQL_Ausgabe": "printSQL.py",
        "DBausgabeFenster": "GUITabelle.py"
    },
    "Verwaltung": {
        "print_SQL_Ausgabe": "printSQL.py",
        "DBinCSV": "CSVExport.py",
        "DBausgabeFenster": "GUITabelle.py"
    },
    "Marketing": {
        "print_SQL_Ausgabe": "printSQL.py",
        "DBausgabeFenster": "GUITabelle.py"
    },
    "Geschäftsführung": {
        "print_SQL_Ausgabe": "printSQL.py",
        "DBinCSV": "CSVExport.py",
        "DBausgabeFenster": "GUITabelle.py",
        "CSV_to_XML": "CSVtoXML.py"
    }
}

# Mapping von Tool-Namen zu Python-Dateien
tool_dateien = {
    "print_SQL_Ausgabe": "printSQL.py",
    "DBinCSV": "CSVExport.py",
    "DBausgabeFenster": "GUITabelle.py",
    "CSV_to_XML": "CSVtoXML.py"
}


# LOGIN-FENSTER
aktuelle_abteilung = None # wie 2.1 einfach default beim starten #########################################################################
# wieder ne haupt klasse (es ist geuaso wie 2.1 (vieleicht paar klinigkeiten geändert) schreibe deswegen keine Commentare.)
class LoginWindow:
    """
    Klasse für das Login-Fenster
    Ermöglicht Authentifizierung der Mitarbeiter
    """
    
    def __init__(self, root):
        """Initialisiert das Login-Fenster"""
        self.root = root
        self.root.title("Heiner IT-Systems - Login")
        self.root.geometry("400x250")
        self.root.resizable(False, False)
        self.center_window()
        self.create_widgets()
    
    def center_window(self):
        """Zentriert das Fenster auf dem Bildschirm"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Erstellt GUI-Elemente für Login"""
        
        # Titel
        title_label = tk.Label(
            self.root,
            text="Heiner IT-Systems GmbH",
            font=("Arial", 16, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(
            self.root,
            text="Mitarbeiter-Verwaltungssystem",
            font=("Arial", 10),
            fg="#7f8c8d"
        )
        subtitle_label.pack()
        
        # Login-Frame
        login_frame = tk.Frame(self.root)
        login_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Abteilungs-Label und Dropdown
        tk.Label(login_frame, text="Abteilung:", font=("Arial", 10), fg="#2c3e50").pack(anchor="w", pady=(0, 5))
        
        self.abteilung_dropdown = ttk.Combobox(
            login_frame,
            values=list(tools_pro_abteilung.keys()),
            state="readonly",
            width=30,
            font=("Arial", 10)
        )
        self.abteilung_dropdown.pack(anchor="w", pady=(0, 15))
        self.abteilung_dropdown.set("-- Abteilung wählen --")
        
        # Passwort-Label und Eingabefeld
        tk.Label(login_frame, text="Passwort:", font=("Arial", 10), fg="#2c3e50").pack(anchor="w", pady=(0, 5))
        
        self.passwort_entry = tk.Entry(login_frame, show="*", width=30, font=("Arial", 10))
        self.passwort_entry.pack(anchor="w", pady=(0, 20))
        self.passwort_entry.bind('<Return>', lambda event: self.login_clicked())
        
        # Button-Frame
        button_frame = tk.Frame(login_frame)
        button_frame.pack(fill="x")
        
        login_button = tk.Button(
            button_frame,
            text="Login",
            command=self.login_clicked,
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        )
        login_button.pack(side="left", padx=(0, 10))
        
        cancel_button = tk.Button(
            button_frame,
            text="Abbrechen",
            command=self.root.quit,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        )
        cancel_button.pack(side="left")
    
    def login_clicked(self):
        """Validiert Login und öffnet Hauptfenster"""
        global aktuelle_abteilung
        
        abteilung = self.abteilung_dropdown.get()
        passwort = self.passwort_entry.get()
        
        # Validierung
        if abteilung == "-- Abteilung wählen --" or abteilung == "":
            messagebox.showerror("Fehler", "Bitte wählen Sie eine Abteilung aus!")
            return
        
        if passwort == "":
            messagebox.showerror("Fehler", "Bitte geben Sie das Passwort ein!")
            return
        
        # Passwort = Abteilungsname
        if passwort != abteilung:
            messagebox.showerror("Fehler", "Passwort ist falsch!")
            self.passwort_entry.delete(0, tk.END)
            return
        
        # Login erfolgreich
        aktuelle_abteilung = abteilung
        self.root.destroy()

##########################################################################################################alles bisher einfach 2.1
# HAUPTFENSTER MIT TOOL-AUSWAHL
class HauptprogrammWindow:
    """
    Klasse für das Hauptfenster
    Zeigt verfügbare Tools basierend auf Abteilung an
    """
    
    def __init__(self, root, abteilung):
        """
        Initialisiert das Hauptfenster
        
        Parameter sind hier einfach :
    root: Tkinter-Hauptfenster
       abteilung: Name der angemeldeten Abteilung
        """
        self.root = root
        self.abteilung = abteilung
        self.root.title(f"Heiner IT-Systems - {abteilung}")
        self.root.geometry("500x400")
        self.center_window()
        self.create_widgets()
    
    def center_window(self):#wieder aus 2.1übernommen
        """Zentriert das Fenster"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        #Erstellt GUI-Elemente für Hauptfenst
        
        # Header
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill="x")
        
        welcome_label = tk.Label(
            header_frame,
            text=f"Willkommen, {self.abteilung}!",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#2c3e50"
        )
        welcome_label.pack(pady=20)
        
        # Tools-Frame
        tools_frame = tk.Frame(self.root)
        tools_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        tk.Label(
            tools_frame,
            text="Verfügbare Tools:",
            font=("Arial", 12, "bold"),
            fg="#2c3e50"
        ).pack(anchor="w", pady=(0, 15))
        
        # Hole verfügbare tools für diese Abteilung
        self.verfuegbare_tools = tools_pro_abteilung.get(self.abteilung, {})
        
        # erstelle Dropdown für Tools
        self.create_dropdown_tools(tools_frame)
        
        # Logout-Button am unteren Ende
        logout_button = tk.Button(
            self.root,
            text="Logout",
            command=self.logout_clicked,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        )
        logout_button.pack(pady=20)
    
    def create_dropdown_tools(self, parent):
        """
        Erstellt ein Dropdown Menü mit verfügbaren toolss
            #parent: Das Parent-Widget für das Dropdown
        """
        
        # Label
        tool_label = tk.Label(
            parent,
            text="Tool auswählen:",
            font=("Arial", 10),
            fg="#2c3e50"
        )
        tool_label.pack(anchor="w", pady=(0, 5))
        
        # Dropdown
        tool_names = list(self.verfuegbare_tools.keys())
        self.tool_dropdown = ttk.Combobox(
            parent,
            values=tool_names,
            state="readonly",
            width=40,
            font=("Arial", 10)
        )
        self.tool_dropdown.pack(anchor="w", pady=(0, 15))
        self.tool_dropdown.set("-- Tool wählen --")
        
        # Button frame
        button_frame = tk.Frame(parent)
        button_frame.pack(fill="x")
        
        # Ausführen bbutton
        execute_button = tk.Button(
            button_frame,
            text="Ausführen",
            command=self.execute_tool,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        )
        execute_button.pack(side="left", padx=(0, 10))
        
        # Beschreibungs-Textbox
        tk.Label(
            parent,
            text="Tool-Beschreibung:",
            font=("Arial", 10, "bold"),
            fg="#2c3e50"
        ).pack(anchor="w", pady=(20, 5))
        
        self.beschreibung_text = tk.Text(
            parent,
            height=8,
            width=50,
            font=("Arial", 9),
            bg="#ecf0f1",
            fg="#2c3e50",
            padx=10,
            pady=10
        )
        self.beschreibung_text.pack(anchor="w", fill="both", expand=True)
        self.beschreibung_text.config(state="disabled")  # Read-only
        
        # Bind Änderungen zum Aktualisieren der Beschreibung
        self.tool_dropdown.bind("<<ComboboxSelected>>", self.update_beschreibung)
    
    def update_beschreibung(self, event=None):
        """
        Aktualisiert die Tool-Beschreibung basierend auf Auswahl
        """
        selected_tool = self.tool_dropdown.get()
        
        # Beschreibungen -- macht das Progeramm ja Benutzerfreundlicher und so...
        beschreibungen = { #das ist einfach ne json artige struktur
            "print_SQL_Ausgabe": "Führt eine SQL-Abfrage aus und zeigt die Ergebnisse\n\n"
                                "Funktion: Alle Mitarbeiter und Artikel aus der Datenbank\n"
                                "Output: Tabelle in der Konsole\n"
                                "Zeitaufwand: ~5 Sekunden",
            
            "DBinCSV": "Exportiert Datenbanktabellen in CSV-Dateien\n\n"
                      "Funktion: Daten in verschiedenen Formaten speichern\n"
                      "Output: CSV-Datei (lagerbestand.csv)\n"
                      "Kompatibilität: Excel, LibreOffice, Google Sheets",
            
            "DBausgabeFenster": "Zeigt Datenbankdaten in einem grafischen Fenster\n\n"
                               "Funktion: Tabellarische Darstellung mit Scrollbar\n"
                               "Output: GUI-Fenster mit interaktiver Tabelle\n"
                               "Sortierung: Durch Klick auf Spaltenköpfe möglich",
            
            "CSV_to_XML": "Konvertiert CSV-Dateien in XML-Format\n\n"
                         "Funktion: Datenformate umwandeln\n"
                         "Input: CSV-Datei\n"
                         "Output: XML-Datei mit strukturierter Hierarchie"
        }
        
        # Aktualisiere Beschreibungstext
        self.beschreibung_text.config(state="normal")
        self.beschreibung_text.delete(1.0, tk.END)
        
        if selected_tool in beschreibungen:
            self.beschreibung_text.insert(1.0, beschreibungen[selected_tool])
        else:
            self.beschreibung_text.insert(1.0, "Bitte wählen Sie ein Tool aus.")
        
        self.beschreibung_text.config(state="disabled")
    
    def execute_tool(self):
        """
        Führt das ausgewählte Tool aus
        """
        selected_tool = self.tool_dropdown.get()
        
        # Validierung
        if selected_tool == "-- Tool wählen --" or selected_tool == "":
            messagebox.showerror("Fehler", "Bitte wählen Sie ein Tool aus!")
            return
        
        # Hole Dateinamen für das Tool
        tool_datei = self.verfuegbare_tools.get(selected_tool)
        
        if not tool_datei:
            messagebox.showerror("Fehler", f"Tool '{selected_tool}' nicht gefunden!")
            return
        
        try:
            # Führe Python-Datei aus
            messagebox.showinfo("Info", f"Starte Tool: {selected_tool}")
            
            # Subprocess zum Ausführen der Python-Datei
            subprocess.Popen([sys.executable, tool_datei])
            
        except FileNotFoundError:
            messagebox.showerror(
                "Fehler",
                f"Datei '{tool_datei}' nicht gefunden!\n\n"
                f"Stelle sicher, dass die Datei im gleichen Verzeichnis existiert."
            )
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Ausführen des Tools:\n{str(e)}")
    
    def logout_clicked(self):
        """Logout und zurück zum Login-Fenster"""
        if messagebox.askyesno("Logout", "Wirklich abmelden?"):
            self.root.destroy()
            # Starte Login-Fenster neu
            start_login()


# MAIN-FUNKTION
def start_login(): 
    """Startet das Login-Fenster"""
    global aktuelle_abteilung #damit die variable auch hier geändert werden kann
    
    root = tk.Tk() #login gernster erstellen wie 2.1
    login_window = LoginWindow(root)
    root.mainloop()
    
    # Nach Login: Starte Hauptprogramm
    if aktuelle_abteilung: # wenn login erfolgreich war => Hauptprogeramm
        root2 = tk.Tk()
        hauptprogramm = HauptprogrammWindow(root2, aktuelle_abteilung)
        root2.mainloop()

if __name__ == "__main__": #start des Progeramms 
    start_login()

