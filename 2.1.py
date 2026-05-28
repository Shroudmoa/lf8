##### Dropdown-Mitarbeiterauswahl mit Passwort-Login 2.1 #####
import tkinter as tk # tkinter für GUI
from tkinter import ttk #ttk für bessere Widgets
from tkinter import messagebox

# Definiere Abteilungen (Mitarbeitergruppen) - USER DICTIONARY 
mitarbeiter_gruppen = {
    "Lager": "Lager",
    "Verwaltung": "Verwaltung",
    "Marketing": "Marketing",
    "Geschäftsführung": "Geschäftsführung"
}

# Globale Variable für aktuell angemeldete Abteilung - immer wird gezigt wenn man den ding startet
aktuelle_abteilung = None
#main app ist einfach class und da haben wir schon alles als funktionen definiert 
class LoginWindow:
    """
    Klasse für das Login-Fenster mit Dropdown-Auswahl
    Ermöglicht Auswahl der Abteilung und Passwortvalidierung
    """
    
    def __init__(self, root):
        """
        Initialisiert das Login-Fenster
        
        Parameter:
            root: Das Tkinter-Hauptfenster
        """
        self.root = root
        self.root.title("Heiner IT-Systems - Login") # kann man ja ändern
        self.root.geometry("400x250") # wie Groß ist das Fenster
        self.root.resizable(False, False) #fixieren oder auch nicht ist an sich egal hier
        
        # Zentriere Fenster auf dem Bildschirm
        self.center_window() #weil es cool ist. 
        
        # Erstelle GUI-Elemente
        self.create_widgets()
    
    def center_window(self): # echt nurtzlos kann man ja auch löschen aber ich hatte diesen Code Block schon fetig.
        """Zentriert das Fenster auf dem Bildschirm"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Erstellt alle GUI-Elemente für das Login-Fenster"""
        
        # Titel
        title_label = tk.Label(
            self.root,
            text="Heiner IT-Systems GmbH",
            font=("Arial", 16, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=20)
        
        # Untertitel
        subtitle_label = tk.Label(
            self.root,
            text="Mitarbeiter-Verwaltungssystem",
            font=("Arial", 10),
            fg="#7f8c8d"
        )
        subtitle_label.pack()
        
        # Frame für Login-Elemente
        login_frame = tk.Frame(self.root)
        login_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Abteilungs-Label
        abteilung_label = tk.Label(
            login_frame,
            text="Abteilung:",
            font=("Arial", 10),
            fg="#2c3e50"
        )
        abteilung_label.pack(anchor="w", pady=(0, 5))
        
        # Abteilungs----Dropdown
        self.abteilung_dropdown = ttk.Combobox(
            login_frame,
            values=list(mitarbeiter_gruppen.keys()),  # Liste aller Abteilungen
            state="readonly",  # Nur Auswahl aus Liste erlaubt
            width=30,
            font=("Arial", 10)
        )
        self.abteilung_dropdown.pack(anchor="w", pady=(0, 15))
        self.abteilung_dropdown.set("-- Abteilung wählen --")  # Standard-Text
        
        # Passwort-Labelll
        passwort_label = tk.Label(
            login_frame,
            text="Passwort:",
            font=("Arial", 10),
            fg="#2c3e50"
        )
        passwort_label.pack(anchor="w", pady=(0, 5))
        
        # PassworEingabefeld
        self.passwort_entry = tk.Entry(
            login_frame,
            show="*",  # Passwort mit Sternen maskieren
            width=30,
            font=("Arial", 10)
        )
        self.passwort_entry.pack(anchor="w", pady=(0, 20))
        
        # Bind Enter-Taste zum Login
        self.passwort_entry.bind('<Return>', lambda event: self.login_clicked())
        
        # Button-Frame
        button_frame = tk.Frame(login_frame)
        button_frame.pack(fill="x")
        
        # Login ------- Button ### einfach als anmerkung labels haben kein command und buttons doch.
        login_button = tk.Button(
            button_frame,
            text="Login",
            command=self.login_clicked,  # Verbinde mit Login-Funktion
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        )
        login_button.pack(side="left", padx=(0, 10))
        
        # Abbrechen-Button
        cancel_button = tk.Button(
            button_frame,
            text="Abbrechen",
            command=self.root.quit,  # Beende Programm
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        )
        cancel_button.pack(side="left")
    
    def login_clicked(self):
        """
        Verarbeitet den Login-Klick
        Validiert Abteilung und Passwort
        """
        global aktuelle_abteilung
        
        # Hole eingegebene Werte
        abteilung = self.abteilung_dropdown.get()
        passwort = self.passwort_entry.get()
        
        # Validierung: Abteilung ausgewählt?  # wieder übertrieben... kann man löschen aber ist doch nett so was zu haben
        if abteilung == "-- Abteilung wählen --" or abteilung == "":
            messagebox.showerror("Fehler", "Bitte wählen Sie eine Abteilung aus!!!!!!")
            return
        
        # Validierung: Passwort eingegeben?
        if passwort == "":
            messagebox.showerror("Fehler", "Bitte geben Sie das Passwort ein!!!!!!")
            return
        
        # Validierung: Passwort korrekt? besser zu sagen Passwort = Benutzername ?
        if passwort != abteilung:
            messagebox.showerror("Fehler", "Passwort ist falsch! schreib einfach den Abteilung Namen")
            self.passwort_entry.delete(0, tk.END)  # Passwortfeld leeren
            return
        
        # Login erfolgreich
        aktuelle_abteilung = abteilung
        messagebox.showinfo("Erfolg", f"Willkommen, {abteilung}!")
        self.root.destroy()  # Schließe Login-Fenster

# Hauptfunktion
if __name__ == "__main__": #starten
    root = tk.Tk() # hauptfenster erstellen
    login_window = LoginWindow(root) # Login Fenster erstellen 
    root.mainloop() # Schleife starten
    
    # Nach dem Login
    if aktuelle_abteilung: # zusätzlich iin cosole schreiben und das wird das Progeramm beeendet
        print(f"Angemeldet als: {aktuelle_abteilung}")
