"""Gegenprobe fuer die Zuordnung Seite -> Suchanfrage in gsc.py.

Die Abfrage page+query ist neu, und ihr gefaehrlichster Fall ist der
leere: eine Seite, deren Anfragen alle anonymisiert sind, liefert null
Zeilen. Wird das stillschweigend uebersprungen, liest sich der Bericht
so, als sei diese Seite in Ordnung -- dabei ist es die einzige, bei der
man das Snippet nicht datengestuetzt schreiben kann.

Drei Faelle:
  positiv    -- Seite mit sichtbaren Anfragen: Tabelle, korrekter Anteil
  negativ    -- Seite ohne sichtbare Anfragen: ausdruecklicher Hinweis
  altbestand -- Daten ohne den Schluessel: kein Absturz, kein Abschnitt
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from gsc import anfragen_je_seite  # noqa: E402

SICHTBAR = {"page": "https://homeeins.de/collections/gartenmobel",
            "position": 2.0, "impressionen": 25, "klicks": 0}
STUMM = {"page": "https://homeeins.de/en/collections/gartenmobel",
         "position": 3.0, "impressionen": 20, "klicks": 0}

DATEN = {"seiten_anfragen": [
    {"page": SICHTBAR["page"], "query": "rattan lounge garten",
     "impressionen": 6, "position": 2.1, "klicks": 0, "ctr": 0},
    {"page": SICHTBAR["page"], "query": "gartenmoebel alu",
     "impressionen": 4, "position": 1.8, "klicks": 0, "ctr": 0},
]}

text = "\n".join(anfragen_je_seite(DATEN, [SICHTBAR, STUMM]))

# Positivfall: die Anfragen stehen da, und der Bezugsrahmen stimmt.
# 10 von 25 Impressionen sind ueber Anfragen sichtbar -> 40 %.
assert "rattan lounge garten" in text, "sichtbare Anfrage fehlt"
assert "gartenmoebel alu" in text, "zweite Anfrage fehlt"
assert "sichtbar: 10 (40 %)" in text, f"Anteil falsch:\n{text}"

# Negativfall: die stumme Seite darf nicht verschwinden. Sie muss
# genannt werden UND als nicht datengestuetzt gekennzeichnet sein.
assert STUMM["page"] in text, "stumme Seite wurde uebersprungen"
assert "Keine einzige Anfrage sichtbar" in text, "leeres Ergebnis unbenannt"
assert "sichtbar: 0 (0 %)" in text, f"Nullanteil falsch:\n{text}"

# Und die Zuordnung darf nicht auslaufen: die Anfragen der einen Seite
# duerfen nicht unter der anderen auftauchen. Text ab der stummen Seite
# abschneiden und dort nachsehen.
schwanz = text.split(f"### {STUMM['page']}", 1)[1]
assert "rattan" not in schwanz, "Anfragen der falschen Seite zugeordnet"

# Altbestand: gsc-aktuell.json aus der Zeit vor dieser Abfrage hat den
# Schluessel nicht. Kein Absturz, aber auch kein leerer Abschnitt.
assert anfragen_je_seite({"seiten": []}, [SICHTBAR]) == [], "Altbestand"

# Keine Null-Klick-Seite -> nichts zu berichten.
assert anfragen_je_seite(DATEN, []) == [], "leere Seitenliste"

print("Positivfall, Negativfall, Trennung und Altbestand bestanden.")
