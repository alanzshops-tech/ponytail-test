"""Gegenprobe fuer die Auswertung in openrouter.py.

Die Arbeitsumgebung erreicht openrouter.ai nicht, der echte Aufruf laeuft
erst auf dem Runner. Was sich hier trotzdem pruefen laesst: dass aus einer
Antwort ein richtiger Bericht wird -- und vor allem, dass ein Fehlschlag
auch als Fehlschlag im Bericht steht und nicht stillschweigend als leere
Tabelle durchgeht. Ein gruener Lauf mit "HTTP 401" im Bericht waere die
schlechteste aller Rueckmeldungen.

Lauf: python3 scripts/probe_openrouter.py
"""
import importlib.util
import sys
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "openrouter", Path(__file__).parent / "openrouter.py")
o = importlib.util.module_from_spec(spec)
sys.argv = ["probe"]
spec.loader.exec_module(o)

GUT = {
    "stand": "2026-08-10",
    "schluessel": {"data": {"label": "homeeins", "limit": 5,
                            "usage": 0.12, "limit_remaining": 4.88,
                            "is_free_tier": False}},
    "guthaben": {"data": {"total_credits": 5, "total_usage": 0.12}},
    "modelle": [
        {"id": "teuer/gross", "name": "Gross", "kontext": 200000,
         "preis_eingabe": 15.0, "preis_ausgabe": 75.0},
        {"id": "billig/klein", "name": "Klein", "kontext": 32000,
         "preis_eingabe": 0.05, "preis_ausgabe": 0.2},
        {"id": "gratis/modell", "name": "Gratis", "kontext": 8000,
         "preis_eingabe": 0.0, "preis_ausgabe": 0.0},
    ],
    "kostenlos": ["gratis/modell"],
    "guenstigstes": "billig/klein",
    "probe": {"modell": "billig/klein", "antwort": "Ein Hundesofa ist ...",
              "verbrauch": {"total_tokens": 42}},
}

SCHLECHT = {
    "stand": "2026-08-10",
    "schluessel": {"fehler": "HTTP 401",
                   "text": '{"error":{"message":"No auth credentials found"}}'},
    "guthaben": {"fehler": "HTTP 401", "text": "..."},
    "modelle": [],
    "probe": {"modell": "billig/klein", "fehler": "HTTP 402",
              "text": '{"error":{"message":"Insufficient credits"}}'},
}


def main() -> int:
    fehler = 0

    b = o.bericht(GUT)
    for muss in ("homeeins", "billig/klein", "0.0500 $", "gratis/modell",
                 "Ein Hundesofa ist", "3 Modelle erreichbar"):
        if muss not in b:
            print(f"FEHLER  Erfolgsfall: '{muss}' fehlt im Bericht"); fehler += 1
    # Das teure Modell muss zwar auftauchen, aber hinter dem billigen.
    if b.index("billig/klein") > b.index("teuer/gross"):
        print("FEHLER  Erfolgsfall: nicht nach Preis sortiert"); fehler += 1
    if not fehler:
        print("OK      Erfolgsfall: Schluessel, Preise, Sortierung, Antwort")

    v = fehler
    b2 = o.bericht(SCHLECHT)
    for muss in ("HTTP 401", "No auth credentials", "HTTP 402",
                 "Insufficient credits", "Fehlgeschlagen"):
        if muss not in b2:
            print(f"FEHLER  Fehlerfall: '{muss}' fehlt im Bericht"); fehler += 1
    # Der Fehlerfall darf nicht wie ein Erfolg aussehen.
    if "Modelle erreichbar" in b2:
        print("FEHLER  Fehlerfall: meldet trotzdem erreichbare Modelle")
        fehler += 1
    if fehler == v:
        print("OK      Fehlerfall: 401 und 402 stehen samt Grund im Bericht")

    # Preisumrechnung: Dollar je Token -> Dollar je Million Token.
    v = fehler
    e, a = o.preis({"pricing": {"prompt": "0.0000005", "completion": "0.0000015"}})
    if round(e, 4) != 0.5 or round(a, 4) != 1.5:
        print(f"FEHLER  Preis falsch umgerechnet: {e}, {a}"); fehler += 1
    # Kaputte Angaben duerfen nicht abstuerzen, sondern muessen 0 ergeben.
    if o.preis({"pricing": {"prompt": None, "completion": "keine Zahl"}}) != (0.0, 0.0):
        print("FEHLER  kaputte Preisangabe nicht abgefangen"); fehler += 1
    if o.preis({}) != (0.0, 0.0):
        print("FEHLER  fehlende Preisangabe nicht abgefangen"); fehler += 1
    if fehler == v:
        print("OK      Preisumrechnung, auch bei fehlenden und kaputten Werten")

    print(f"\nFehlschlaege: {fehler}")
    return 1 if fehler else 0


if __name__ == "__main__":
    raise SystemExit(main())
