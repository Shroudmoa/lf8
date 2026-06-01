##### CSV-Datei in XML umwandeln #####

import csv
import xml.etree.ElementTree as ET #XML-Struktur bauen
import xml.dom.minidom as minidom #pretty print 

def csv_to_xml(input_file, output_file):
    """
    Konvertiert eine CSV-Datei in ein XML-Dokument
    
    Parameter:
        input_file: Name der CSV-Eingabedatei
        output_file: Name der XML-Ausgabedatei
    """
    try:
        # Erstelle Root-Element
        root = ET.Element('Datenbank')#<DB>  </DB> Start point
        
        # Öffne und lese CSV-Datei
        with open(input_file, 'r', encoding='utf-8') as csvfile:#r => read
            csv_reader = csv.DictReader(csvfile, delimiter=';')  # Lese mit Spaltennamen
            
            # Verarbeite jede Zeile
            for row in csv_reader:
                # Erstelle Element für jede Zeile
                item = ET.SubElement(root, 'Datensatz') #Jede CSV-Zeile wird einzeln bearbeitet.
                
                # Füge jedes Feld als Unterelement hinzu
                for key, value in row.items(): 
                    field = ET.SubElement(item, key)#key wäre z.B "name" daraus wir <Name> erzeugt
                    field.text = str(value) if value else ""
        
        # Formatiere und schreibe XML
        xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ") #pretty print default code 
        
        # Entferne die erste XML-Deklarationszeile (wird doppelt erzeugt)
        xml_str = '\n'.join(xml_str.split('\n')[1:])
        
        with open(output_file, 'w', encoding='utf-8') as xmlfile: #w => write
            xmlfile.write(xml_str)
        
        print(f"XML-Konvertierung erfolgreich: {output_file}")
        
    except FileNotFoundError as e:
        print(f"Fehler: Datei nicht gefunden - {e}")
    except Exception as e:
        print(f"Fehler bei der Konvertierung: {e}")

# Beispiel: CSV-Datei in XML konvertieren
csv_to_xml("lagerbestand.csv", "lagerbestand.xml")
