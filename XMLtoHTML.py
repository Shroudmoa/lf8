##### XML-Datei als HTML-Webseite darstellen #####

import xml.etree.ElementTree as ET #ermöglicht lesen und schreiben von xml.dateien

def xml_to_html(xml_file, html_output_file):
    """
    Konvertiert eine XML-Datei in ein HTML-Dokument und stellt es tabellarisch dar
    
    Parameter:
        xml_file: Name der XML-Eingabedatei
        html_output_file: Name der HTML-Ausgabedatei
    
    Zweck: 
        - XML-Daten in einem Web-Browser visuell darstellen
        - Bessere Lesbarkeit für nicht-technische Benutzer
        - Ermöglicht einfaches Drucken und Weitergabe der Daten
    """
    try:
        # Parse XML-Datei
        tree = ET.parse(xml_file)#einfach geasgt öffnet XML und liest die Datei
        root = tree.getroot() 
        
        # Ermittle Spaltennamen aus dem ersten Datensatz
        first_record = root.find('Datensatz')#einfach checken ob wir eine XML Datei haben oder nicht
        if first_record is None:
            print("Keine Datensätze in XML gefunden!")
            return
        
        columns = [child.tag for child in first_record] #tags lesen. keine Werte 
        
        # Erstelle HTML-Struktur kann man ja auch weniger schreiben => CSS braucht man ja nicht oder copyright symbol am ENDE
        html_content = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Heiner IT-Systems - Datenverwaltung</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        th {
            background-color: #2c3e50;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }
        td {
            padding: 10px 12px;
            border-bottom: 1px solid #ddd;
        }
        tr:hover {
            background-color: #f9f9f9;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            color: #666;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <h1>Heiner IT-Systems - Datenverwaltung</h1>
    <table>
        <thead>
            <tr>
"""
        
        # Füge Spaltenköpfe hinzu
        for col in columns:
            html_content += f"                <th>{col}</th>\n"
        
        html_content += """            </tr>
        </thead>
        <tbody>
"""
        
        # Füge Datensätze hinzu
        for record in root.findall('Datensatz'):
            html_content += "            <tr>\n"
            for col in columns:
                value = record.find(col)
                text = value.text if value is not None and value.text else "-"
                html_content += f"                <td>{text}</td>\n"
            html_content += "            </tr>\n"
        
        html_content += """        </tbody>
    </table>
    <div class="footer">
        <p>Generiert von Heiner IT-Systems | © 2077</p>
    </div>
</body>
</html>
"""
        """
        XML => 
        <Datensatz>
    <Artikelnummer>1001</Artikelnummer>
    <Artikel>Notebook</Artikel>
    <Bestand>15</Bestand>
        </Datensatz>
        HTML Kopf => 
       <tr>
    <th>Artikelnummer</th>
    <th>Artikel</th>
    <th>Bestand</th>
       </tr>

    ####################################
    <tr>
    <td>1001</td>
    <td>Notebook</td>
    <td>15</td>
     </tr>
        """
        # Schreibe HTML-Datei
        with open(html_output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"HTML-Export erfolgreich: {html_output_file}")
        
    except FileNotFoundError as e:
        print(f"Fehler: Datei nicht gefunden - {e}")
    except Exception as e:
        print(f"Fehler: {e}")

# Aufruf der Funktion
xml_to_html("lagerbestand.xml", "lagerbestand.html")
