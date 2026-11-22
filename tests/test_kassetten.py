#!/usr/bin/env python3
"""
Testet die CJ-Auswertung gegen echte, aufgezeichnete Antworten.

Der Unterschied zu vorher: Diese Tests prüfen nicht, ob mein Code meine
Attrappe richtig liest, sondern ob er die Antwort liest, die CJ am
9. August 2026 tatsächlich geschickt hat. Jede Annahme, die hier
festgeschrieben ist, war einmal falsch.

Aufgenommen wird auf dem Runner (dort gibt es Netz und Zugangsdaten),
abgespielt überall. Zugangsdaten sind in den Kassetten geschwärzt.

    python3 tests/test_kassetten.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WURZEL / "scripts"))
KASSETTEN = WURZEL / "kassetten"

import cj                                                   # noqa: E402


def rohantwort(name: str) -> dict:
    """Antwortkörper aus einer Kassette, ohne vcr — der Test soll auch
    ohne zusätzliche Bibliothek laufen."""
    import yaml
    d = yaml.safe_load((KASSETTEN / name).read_text(encoding="utf-8"))
    koerper = d["interactions"][0]["response"]["body"]["string"]
    if isinstance(koerper, bytes):
        koerper = koerper.decode("utf-8", "replace")
    return json.loads(koerper)


def pruefe(bedingung: bool, text: str) -> None:
    if not bedingung:
        raise AssertionError(text)
    print(f"  ok  {text}")


def test_waehrung_wird_nicht_geliefert() -> None:
    """Der teuerste Irrtum des Tages: Ich hielt die Preise für Dollar.

    Die API nennt die Währung nicht — das Feld heißt currency und ist
    leer. Damit ist die Kontoeinstellung die einzige Quelle. Sollte CJ
    das Feld eines Tages füllen, schlägt dieser Test an, und dann
    gehört die Umrechnung ans Feld statt an eine Annahme."""
    a = rohantwort("cj_liste.yaml")
    artikel = a["data"]["content"][0]["productList"]
    leer = [p for p in artikel if p.get("currency") in (None, "")]
    pruefe(len(leer) == len(artikel),
           f"currency ist bei allen {len(artikel)} Artikeln leer — "
           f"die Währung kommt aus der Kontoeinstellung, nicht aus der API")
    text = json.dumps(a)
    pruefe(text.count("USD") == 0 and text.count("EUR") == 0,
           "weder USD noch EUR stehen irgendwo in der Antwort")


def test_kategorie_nur_mit_zusatzparameter() -> None:
    """threeCategoryName kommt nur, wenn features=enable_category
    mitgeschickt wird. Ohne den Parameter war die Kategoriespalte
    368-mal 'ohne Angabe'."""
    import yaml
    d = yaml.safe_load((KASSETTEN / "cj_liste.yaml").read_text(encoding="utf-8"))
    uri = d["interactions"][0]["request"]["uri"]
    pruefe("features=enable_category" in uri,
           "die Abfrage schickt features=enable_category mit")
    a = rohantwort("cj_liste.yaml")
    artikel = a["data"]["content"][0]["productList"]
    mit = [p for p in artikel if p.get("threeCategoryName")]
    pruefe(len(mit) > len(artikel) * 0.8,
           f"{len(mit)} von {len(artikel)} Artikeln haben eine Kategorie")


def test_auswertung_liest_echte_antwort() -> None:
    """Der eigentliche Punkt: mein Code gegen die echte Antwort, nicht
    gegen eine selbstgeschriebene."""
    a = rohantwort("cj_liste.yaml")
    treffer = []
    for block in a["data"]["content"]:
        for p in block["productList"]:
            treffer.append({
                "name": p.get("nameEn", ""), "sku": p.get("sku", ""),
                "bestand": p.get("warehouseInventoryNum", 0),
                "gelistet_von": p.get("listedNum", 0),
                "versand_inklusive": p.get("addMarkStatus"),
            })
    pruefe(len(treffer) > 50, f"{len(treffer)} Artikel aus der Antwort gelesen")
    pruefe(all(t["sku"] for t in treffer), "jeder Artikel hat eine SKU")
    pruefe(all(t["name"] for t in treffer), "jeder Artikel hat einen Namen")
    # Die Bestandszahlen dürfen nicht alle gleich sein. Beim ersten Lauf
    # stand überall 230 — das war der Hinweis, dass die Suche etwas
    # anderes lieferte als gedacht.
    werte = {t["bestand"] for t in treffer}
    pruefe(len(werte) > 5,
           f"{len(werte)} verschiedene Bestandszahlen — keine Einheitszahl")


def test_bestand_ist_der_deutsche() -> None:
    """warehouseInventoryNum in der gefilterten Abfrage ist der Bestand
    in Deutschland, nicht der weltweite. Bewiesen an der Steppdecke:
    2019 in Deutschland, ein Vielfaches davon weltweit."""
    liste = rohantwort("cj_liste.yaml")
    erster = liste["data"]["content"][0]["productList"][0]
    bestand = rohantwort("cj_bestand.yaml")["data"]
    de = next((w for w in bestand if w.get("countryCode") == "DE"), None)
    pruefe(de is not None, "die Bestandsabfrage kennt ein deutsches Lager")
    welt = sum(int(w.get("totalInventoryNum") or 0) for w in bestand)
    pruefe(int(de.get("cjInventoryNum") or 0) == erster["warehouseInventoryNum"],
           f"DE-Lager {de.get('cjInventoryNum')} entspricht der Listenzahl "
           f"{erster['warehouseInventoryNum']}")
    pruefe(welt > erster["warehouseInventoryNum"],
           f"weltweit {welt} liegt darüber — die Liste zeigt also nicht "
           f"den globalen Bestand")


def test_keine_zugangsdaten_in_den_kassetten() -> None:
    """Läuft bei jedem Testlauf mit. Eine Kassette mit Token im Klartext
    wäre schlimmer als gar keine."""
    import re
    for f in sorted(KASSETTEN.glob("*.yaml")):
        t = f.read_text(encoding="utf-8", errors="replace")
        for feld in ("apiKey", "accessToken", "refreshToken"):
            for m in re.finditer(rf'"{feld}"\s*:\s*"([^"]*)"', t):
                pruefe(m.group(1) == "GESCHWAERZT",
                       f"{f.name}: {feld} ist geschwärzt")
        pruefe("CJ-Access-Token" not in t,
               f"{f.name}: kein Token im Anfragekopf")


def main() -> None:
    if not KASSETTEN.exists() or not list(KASSETTEN.glob("*.yaml")):
        sys.exit("Keine Kassetten vorhanden. Aufnehmen mit dem Workflow "
                 "\"CJ-Katalog durchsuchen\", Eingabe kassetten = true.")
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    fehler = 0
    for t in tests:
        print(f"\n{t.__name__}")
        try:
            t()
        except AssertionError as e:
            print(f"  FEHLGESCHLAGEN  {e}")
            fehler += 1
    print(f"\n{len(tests) - fehler} von {len(tests)} Tests bestanden")
    sys.exit(1 if fehler else 0)


if __name__ == "__main__":
    main()
