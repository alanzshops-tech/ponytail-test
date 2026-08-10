"""Gegenprobe fuer die Messgeraete in modellprobe.py.

Ein Selektor, der zu viel faengt, ist kein Messgeraet. In diesem Projekt
ist das dreimal passiert -- "Ausverkauft" im Theme-Template, "Rechnung" in
"Rechnungsadresse", Judge.mes Einstellungs-Script statt des Widgets.
Deshalb steht hier zu jedem Muster ein Fall, der treffen MUSS, und einer,
der NICHT treffen darf.

Lauf: python3 scripts/probe_modellprobe.py
"""
import importlib.util
import sys
from pathlib import Path

for name in ("openrouter", "modellprobe"):
    spec = importlib.util.spec_from_file_location(
        name, Path(__file__).parent / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.argv = ["probe"]
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
m = sys.modules["modellprobe"]

ANGABEN = ("Titel: Premium Gewichtsdecke\nPreis: 74,00 €\n"
           "Varianten: Blau / 135 x 200 cm / 10 kg")

# (Beschreibung, Text, was herauskommen muss)
ZAHLEN = [
    ("Masse aus der Aufgabe uebernommen",
     "Die Decke misst 135 x 200 cm und wiegt 10 kg.", []),
    ("Waschtemperatur erfunden",
     "Die Decke ist bei 60 Grad waschbar.", ["60"]),
    ("Fuellgewicht erfunden",
     "Mit 3200 Glasperlen gefüllt.", ["3200"]),
    ("kleine Zaehlzahl ist keine Zusicherung",
     "In zwei Größen und 3 Farben erhältlich.", []),
    ("Preis aus der Aufgabe",
     "Für 74,00 € erhältlich.", []),
    ("Komma und Punkt sind dieselbe Zahl",
     "Sie wiegt 10.0 kg.", []),
]

MASCHEN = [
    # (Muster-Name, Text der treffen MUSS, Text der NICHT treffen darf)
    ("Knappheit", "Nur noch 3 Stück auf Lager.",
     "Die Decke macht das Zubettgehen nur noch angenehmer."),
    ("Zeitdruck", "Nur heute zum Vorteilspreis.",
     "Sie eignet sich nur für Doppelbetten."),
    ("Streichpreis", "Jetzt 74,00 € statt 99,00 €.",
     "Der Preis liegt bei 74,00 € statt eines Abos."),
    ("Publikum", "27 Personen sehen sich das gerade an.",
     "Zwei Personen finden darunter Platz."),
    ("Rang", "Unser Bestseller im Schlafzimmer.",
     "Die Decke ist bei Rückenschläfern beliebt."),
]

ENGLISCH = [
    ("englischer Satzrest", "This blanket is soft and warm.", True),
    ("deutscher Text mit Lehnwoertern",
     "Das Set im schlichten Design sorgt für Komfort.", False),
    ("Marke mit englischem Wort im Titel",
     "Die Decke aus der Premium-Reihe wiegt 10 kg.", False),
]


def main() -> int:
    fehler = 0

    for name, text, erwartet in ZAHLEN:
        ist = m.erfundene_zahlen(text, ANGABEN)
        if ist != erwartet:
            print(f"FEHLER  Zahlen/{name}: erwartet {erwartet}, bekommen {ist}")
            fehler += 1
    if not fehler:
        print("OK      erfundene Zahlen: Masse erkannt, Zaehlzahlen ignoriert")

    v = fehler
    for name, trifft, trifft_nicht in MASCHEN:
        if name not in m.maschen(trifft):
            print(f"FEHLER  Masche/{name}: Positivfall nicht erkannt "
                  f"({trifft!r})")
            fehler += 1
        if name in m.maschen(trifft_nicht):
            print(f"FEHLER  Masche/{name}: Fehlalarm bei {trifft_nicht!r}")
            fehler += 1
    if fehler == v:
        print("OK      Dark Patterns: alle fünf Muster, je Treffer und "
              "Nicht-Treffer")

    v = fehler
    for name, text, soll in ENGLISCH:
        ist = bool(m.englisch(text))
        if ist != soll:
            print(f"FEHLER  Englisch/{name}: erwartet {soll}, bekommen "
                  f"{m.englisch(text)}")
            fehler += 1
    if fehler == v:
        print("OK      englische Reste: erkannt, ohne Lehnwörter zu fangen")

    # Der Bericht muss einen Fehlschlag als solchen zeigen und nicht als
    # leere Zeile durchgehen lassen.
    v = fehler
    b = m.bericht({"stand": "x", "modelle": {
        "kaputt/modell": [{"aufgabe": "a", "fehler": "HTTP 429", "dauer": 0.2}],
        "gut/modell": [{"aufgabe": "a", "antwort": "Ein Text.", "dauer": 1.0,
                        "woerter": 2, "erfundene_zahlen": [], "maschen": [],
                        "englisch": [], "kosten": 0, "token": 9}],
    }})
    for muss in ("kaputt/modell", "HTTP 429", "gut/modell", "Ein Text."):
        if muss not in b:
            print(f"FEHLER  Bericht: '{muss}' fehlt"); fehler += 1
    if fehler == v:
        print("OK      Bericht: Fehlschlag und Erfolg beide sichtbar")

    print(f"\nFehlschlaege: {fehler}")
    return 1 if fehler else 0


if __name__ == "__main__":
    raise SystemExit(main())
